# Эхнээс нь ажиллуулах ба даалгавар өгөх

## А. Шинэ аппыг ажиллуулах

1. personal_finance_complete.zip татна.
2. Downloads дотор ZIP дээр хулганы баруун товч → Extract All → Extract.
3. Задалсан хавтас дотор finance.py, requirements.txt зэрэг файлууд байгаа.
4. Хуучин аппын VS Code Terminal дээр Ctrl+C дарж зогсооно.
5. C:\Users\ezutr\huulga доторх finance_account.db, finance.db файлуудаа
   байвал өөр хавтаст нөөцөлнө. Устгахгүй.
6. Задалсан багцын файлуудыг C:\Users\ezutr\huulga дотор хуулна.
   finance.py-г солих асуултад Replace сонгоно. ZIP дотор .db файл байхгүй.
7. VS Code → File → Open Folder → C:\Users\ezutr\huulga → Select Folder.
8. Terminal → New Terminal. Дараахыг нэг нэгээр нь ажиллуулна:

```powershell
cd "C:\Users\ezutr\huulga"
python -m pip install -r requirements.txt
python -m streamlit run finance.py
```

9. Терминалын Local URL холбоосыг нээнэ. Ихэвчлэн http://localhost:8501.
   Имэйл асуувал хоосон Enter. Терминалыг нээлттэй байлгана.
10. Гарчиг «Миний санхүү — Төсөв ба зорилго» болсон байна.
    Цэсэнд «Төсөв ба гүйцэтгэл», «Урт хугацааны зорилго» гарна.

Дараа дахин асаахдаа start_finance.bat дээр хоёр товшиж болно.

## Б. Гурван шаардлагыг шалгаж үзэх

### 1. Импорт

AI-г эхлээд унтраалттай үлдээнэ. account-statement хуулгаа сонгоод импортолно.
Өмнөх энэ сан дахь ижил хуулга байвал дахин нэмэхгүй.
Дараагийн хугацааны account хуулгыг импортлоход шинэ гүйлгээ нэмэгдэнэ.

### 2. Төсөв

«Төсөв ба гүйцэтгэл» → сар 2026-11.
- Төрөл Орлого, ангилал Цалин, төлөвлөсөн дүн 2,000,000 → Төсөв хадгалах.
- Төрөл Зарлага, ангилал Хүнс, дүн 400,000 → Төсөв хадгалах.
- Бусад ангиллыг ижил аргаар нэмнэ.
Хуулгатай сар сонговол гүйцэтгэл нь бодит гүйлгээнээс гарна.

### 3. Зорилго

«Урт хугацааны зорилго» → Шинэ зорилго. Жишээ нь:
- Нэр: Машин
- Үнэ: 24,000,000 ₮
- Эхний хуримтлал: 6,000,000 ₮
- Нэмэлт эх үүсвэр: 2,000,000 ₮
- Зээл: 10,000,000 ₮
- Жилийн хүү: 12%
- Зээлийн хугацаа: 60 сар
- Эхлэх сар: 2026-11
- Хүрэх сар: 2027-10
- Сарын төсөвт автоматаар оруулах: идэвхтэй

Тооцоолж хадгалах дарна. Шинээр хуримтлуулах 6,000,000 ₮ буюу сард 500,000 ₮ гарна.
2026-11 сарын төсөвт Машины хуримтлал автоматаар орсон байна.
2027-11 сарын төсөвт зээлийн төлбөр орно.
Байр зэрэг өөр зорилгыг нэмж болно; хоёр зорилгын төлөвлөгөө төсөвт хамт харагдана.
Хадгаламж руу шилжүүлсэн бодит гүйлгээг доорх «Бодит гүйлгээг зорилготой холбох»
хэсэгт сонгоод зорилго, зориулалт, дүн оруулж хадгална.

## В. GitHub repository үүсгэх

Энэ багцыг бэлтгэх үед GitHub repository үүсгэж, collaborator урилга илгээгээгүй.
Дараах алхмуудыг өөрийн GitHub бүртгэлээр гүйцэтгэнэ.

1. https://github.com руу орж Sign in. Бүртгэлгүй бол Sign up.
2. https://github.com/new нээнэ.
3. Repository name: personal-finance-app.
4. Description: Personal finance app with Excel import, budgets and financial goals.
5. Private сонгож болно. Багш Public шаардсан бол Public сонго.
6. Add README сонгохгүй (багцад README.md байгаа).
7. Create repository дарна.
8. Хоосон repository дээр uploading an existing file холбоос дарна.
   Файлтай repository бол Add file → Upload files.
9. Зөвхөн дараах файлуудыг сонгож оруулна:
   finance.py, requirements.txt, README.md, SETUP_MN.md,
   test_finance.py, start_finance.bat, .gitignore.
10. Commit message хэсэгт Add personal finance app бичээд Commit changes дарна.
    Хэрэв шинэ branch/Propose changes гэсэн урсгал гарвал санал болгосон
    өөрчлөлтөөс Pull request үүсгэж, өөрийн repository-д Merge pull request дарна.
11. Repository-ийн Code хэсэгт дээрх файлууд харагдаж байгааг шалгана.

Банкны Excel, .db, нууц үг, API түлхүүрийг оруулахгүй. Upload files дээр бүх huulga
хавтсаа чирч оруулж болохгүй. .gitignore нь браузераар гараар сонгосон нууц файлыг
автоматаар хориглох хамгаалалт биш.

## Г. ankhbayar-ufe-ийг Collaborator болгох

1. Шинэ repository дотроо Settings дарна.
2. Зүүн талын Access → Collaborators.
3. Нууц үг/баталгаажуулалт асуувал өөрийн бүртгэлээр баталгаажуулна.
4. Add people дарна.
5. ankhbayar-ufe гэж яг бичнэ.
6. Гарч ирсэн үр дүнгийн username нь яг ankhbayar-ufe гэдгийг шалгаж сонгоно.
7. Add ankhbayar-ufe to personal-finance-app дарна.
8. Pending invitation гэвэл урилга илгээгдсэн боловч хараахан хүлээж аваагүй.
   Урилгыг хүлээн авсны дараа collaborator эрхтэй болно.

## Д. Даалгаварт илгээх холбоос

Repository-ийн Code үндсэн хуудсыг нээгээд браузерын хаягийг хуулна.
Хэлбэр: https://github.com/ТАНЫ_USERNAME/personal-finance-app
Энэ нь жишээ хэлбэр; ТАНЫ_USERNAME гэж шууд хуулж өгөхгүй.
localhost:8501, ZIP татах холбоос эсвэл нэг finance.py файлын холбоос өгөхгүй.
Багшид repository холбоос болон collaborator урилга илгээсэн төлөвөө хэлнэ.

Албан ёсны заавар:
https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository
