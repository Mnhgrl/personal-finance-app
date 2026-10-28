import ast
import io
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

source = Path(__file__).with_name('finance.py')
tree = ast.parse(source.read_text(encoding='utf-8').split('# ==================== АППЫН ЭХЛЭЛ')[0])
tree.body = [n for n in tree.body if not isinstance(n, ast.Expr) and not (
    isinstance(n, ast.Import) and any(a.name == 'streamlit' for a in n.names))]
app = types.ModuleType('finance_core')
app.__file__ = str(source)
exec(compile(tree, str(source), 'exec'), app.__dict__)

class FinanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        app.DATABASE = Path(self.tmp.name) / 'test.db'
        app.create_tables()
        app.create_planning_tables()
        app.CLASSIFIER = app.LocalClassifier(False)

    def tearDown(self):
        self.tmp.cleanup()

    def goal(self, **overrides):
        g = dict(name='Машин', target=2400000, initial=600000, gift=200000,
                 loan=1000000, annual_rate=0, loan_months=10,
                 start_month='2026-11', target_month='2027-02', active=1)
        g.update(overrides)
        return g

    def tx(self, txid='one', amount=-10000, date='2026-11-12', kind='Зарлага'):
        with app.connect_db() as c:
            c.execute('INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?,?)',
                (txid,'test',date,'test transfer','test',amount,'Бусад',kind,0,'demo'))

    def test_budget_upsert_and_month_isolation(self):
        app.save_budget('2026-11','Хүнс','Зарлага',10000)
        app.save_budget('2026-11','Хүнс','Зарлага',20000)
        self.assertEqual(app.budget_report('2026-11')['Төсөв ₮'].sum(),200)
        self.assertTrue(app.budget_report('2026-12').empty)

    def test_month_rollover_and_validation(self):
        self.assertEqual(app.move_month('2026-12',1),'2027-01')
        with self.assertRaises(ValueError): app.month_number('2026-13')

    def test_mixed_financing_and_loan_timing(self):
        g = self.goal();p=app.goal_plan(g)
        self.assertEqual(p['need'],600000)
        self.assertEqual(p['saving'],150000)
        self.assertEqual(p['payment'],100000)
        app.save_goal(g)
        self.assertEqual(app.budget_report('2026-11')['Төсөв ₮'].sum(),1500)
        self.assertEqual(app.budget_report('2027-02')['Төсөв ₮'].sum(),1500)
        self.assertEqual(app.budget_report('2027-03')['Төсөв ₮'].sum(),1000)
        self.assertTrue(app.budget_report('2028-01').empty)

    def test_annuity_known_value_and_rounding(self):
        self.assertEqual(app.loan_payment(100000000,12,12),8884879)
        p=app.goal_plan(self.goal(target=100, initial=0,gift=0,loan=0,
                      start_month='2026-11', target_month='2027-01'))
        self.assertEqual(p['saving'],34)
        gid=app.save_goal(self.goal(target=100,initial=0,gift=0,loan=0,
                         start_month='2026-11',target_month='2027-01'))
        self.assertAlmostEqual(sum(app.budget_report(m)['Төсөв ₮'].sum()
                           for m in ['2026-11','2026-12','2027-01']),1)

    def test_invalid_goal(self):
        for g in [self.goal(target=1),self.goal(target_month='2026-01'),
                  self.goal(initial=-1),self.goal(annual_rate=-1)]:
            with self.assertRaises(ValueError): app.save_goal(g)

    def test_allocation_no_double_count_and_update(self):
        gid=app.save_goal(self.goal());self.tx()
        app.allocate_transaction('one',gid,'Хуримтлал',6000)
        report=app.budget_report('2026-11')
        self.assertEqual(report['Гүйцэтгэл ₮'].sum(),100)
        self.assertEqual(report.loc[report['Ангилал']=='Бусад','Гүйцэтгэл ₮'].iloc[0],40)
        app.allocate_transaction('one',gid,'Хуримтлал',7000)
        self.assertEqual(app.budget_report('2026-11')['Гүйцэтгэл ₮'].sum(),100)
        with self.assertRaises(ValueError):app.allocate_transaction('one',gid,'Зээлийн төлбөр',4000)
        with self.assertRaises(ValueError):app.allocate_transaction('one',gid,'Хуримтлал',10001)

    def test_savings_and_internal_transfer(self):
        gid=app.save_goal(self.goal());self.tx(kind='Өөрийн данс хооронд')
        self.assertEqual(app.budget_report('2026-11')['Гүйцэтгэл ₮'].sum(),0)
        app.allocate_transaction('one',gid,'Хуримтлал',10000)
        self.assertEqual(app.budget_report('2026-11')['Гүйцэтгэл ₮'].sum(),100)
        self.tx(txid='deposit',amount=10000,kind='Өөрийн данс хооронд')
        self.assertEqual(app.budget_report('2026-11')['Гүйцэтгэл ₮'].sum(),100)

    def test_multiple_goals_and_inactive(self):
        a=app.save_goal(self.goal());b=app.save_goal(self.goal(name='Байр'))
        self.assertEqual(app.budget_report('2026-11')['Төсөв ₮'].sum(),3000)
        app.save_goal(self.goal(active=0),a)
        self.assertEqual(app.budget_report('2026-11')['Төсөв ₮'].sum(),1500)

    def table(self):
        rows=[[None]*9 for _ in range(6)]
        rows[0][0]='Дансны дугаар:';rows[0][1]='123'
        rows[0][4]='Эхний үлдэгдэл:';rows[0][6]='100'
        rows[1][4]='Эцсийн үлдэгдэл:';rows[1][6]='90'
        rows[2][0]='Огноо';rows[2][2]='Орлого';rows[2][3]='Зарлага'
        rows[3][0]='2026-11-01 10:00:00';rows[3][3]='-10';rows[3][7]='90';rows[3][8]='KFC'
        rows[4][0]='Нийт:';rows[4][2]=0;rows[4][3]=10
        return app.pd.DataFrame(rows)

    def test_import_repeat_and_manual_preserved(self):
        b=io.BytesIO(b'first');b.name='anything.xlsx'
        with patch.object(app.pd,'read_excel',return_value=self.table()):
            self.assertEqual(app.import_file(b)['added'],1)
            self.assertTrue(app.import_file(b)['already_imported'])
            with app.connect_db() as c:c.execute("UPDATE transactions SET category='Custom',manual=1")
            b=io.BytesIO(b'another_export');b.name='renamed.xlsx'
            self.assertEqual(app.import_file(b)['duplicates'],1)
        self.assertEqual(app.get_transactions().iloc[0]['category'],'Custom')

    def test_import_balance_failure_is_atomic(self):
        table=self.table();table.iloc[3,7]='89'
        b=io.BytesIO(b'bad');b.name='bad.xlsx'
        with patch.object(app.pd,'read_excel',return_value=table):
            with self.assertRaises(ValueError):app.import_file(b)
        self.assertTrue(app.get_transactions().empty)

    def test_next_period_appends(self):
        b=io.BytesIO(b'nov');b.name='nov.xlsx'
        with patch.object(app.pd,'read_excel',return_value=self.table()):app.import_file(b)
        table=self.table();table.iloc[3,0]='2026-12-01 10:00:00'
        b=io.BytesIO(b'dec');b.name='dec.xlsx'
        with patch.object(app.pd,'read_excel',return_value=table):self.assertEqual(app.import_file(b)['added'],1)
        self.assertEqual(len(app.get_transactions()),2)

if __name__=='__main__':unittest.main()
