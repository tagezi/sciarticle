--
-- Файл сгенерирован с помощью SQLiteStudio v3.3.3 в чт февр. 17 10:50:35 2022
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: AcademicAffiliation
DROP TABLE IF EXISTS AcademicAffiliation;
CREATE TABLE AcademicAffiliation (id_aa INTEGER PRIMARY KEY, id_publisher INTEGER REFERENCES Publisher (id_publisher), affiliation);

-- Таблица: Author
DROP TABLE IF EXISTS Author;
CREATE TABLE Author (id_author INTEGER PRIMARY KEY, author_name TEXT (50) NOT NULL, last_name TEXT (20), first_name TEXT (30),
 initials TEXT (3), birth_date DATE, id_scientific_title INTEGER);

-- Таблица: Book
DROP TABLE IF EXISTS Book;
CREATE TABLE Book (id_book INTEGER PRIMARY KEY, book_name TEXT, creation_year INTEGER, publisher INTEGER REFERENCES Publisher (id_publisher), book_frequency TEXT, iso_4 TEXT, issn_print TEXT, issn_web TEXT, book_homepage TEXT, online_access TEXT, online_archive TEXT, wiki_url TEXT);

-- Таблица: BookCodes
DROP TABLE IF EXISTS BookCodes;
CREATE TABLE BookCodes (id_book_code INTEGER PRIMARY KEY, id_book INTEGER REFERENCES Book (id_book), bluebook TEXT, mathscinet TEXT, nlm TEXT, coden TEXT, jstor TEXT, lccn TEXT, oclc TEXT, asin TEXT, bici TEXT, estc TEXT, ettn TEXT, istc TEXT, sici TEXT);

-- Таблица: BookDiscipline
DROP TABLE IF EXISTS BookDiscipline;
CREATE TABLE BookDiscipline (id_book_discipline INTEGER PRIMARY KEY, id_book INTEGER REFERENCES Book (id_book),
 id_discipline INTEGER REFERENCES Discipline (id_discipline));

-- Таблица: BookEditor
DROP TABLE IF EXISTS BookEditor;
CREATE TABLE BookEditor (id_book_editor INTEGER PRIMARY KEY, id_book INTEGER REFERENCES Book (id_book) NOT NULL, editor TEXT NOT NULL);

-- Таблица: BookLang
DROP TABLE IF EXISTS BookLang;
CREATE TABLE BookLang (id_book_lang INTEGER PRIMARY KEY, id_book INTEGER REFERENCES Book (id_book), id_lang INTEGER REFERENCES Lang (id_lang));

-- Таблица: Country
DROP TABLE IF EXISTS Country;
CREATE TABLE Country (id_country INTEGER PRIMARY KEY, en_name_country TEXT NOT NULL, ru_name_country TEXT, official_en_name TEXT,
 sovereignty TEXT, alpha_2_code TEXT, alpha_3_code TEXT, numeric_code INTEGER, subdivision_code TEXT, internet_cctld TEXT);

-- Таблица: Discipline
DROP TABLE IF EXISTS Discipline;
CREATE TABLE Discipline (id_discipline INTEGER PRIMARY KEY, discipline_name TEXT, discipline_url TEXT);

-- Таблица: Keywords
DROP TABLE IF EXISTS Keywords;
CREATE TABLE Keywords (id_keyword INTEGER PRIMARY KEY, keyword TEXT NOT NULL);

-- Таблица: Lang
DROP TABLE IF EXISTS Lang;
CREATE TABLE Lang (id_lang INTEGER PRIMARY KEY, lang TEXT (20) NOT NULL, iso_639_1 TEXT, iso_639_2 TEXT, iso_639_3 TEXT,
 iso_639_5 TEXT, gost_7_75_lat TEXT, gost_7_75_rus TEXT, d_code TEXT);

-- Таблица: LangVariant
DROP TABLE IF EXISTS LangVariant;
CREATE TABLE LangVariant (id_lang_variant INTEGER PRIMARY KEY, id_lang INTEGER REFERENCES Lang (id_lang), lang TEXT);

-- Таблица: PublicationAuthor
DROP TABLE IF EXISTS PublicationAuthor;
CREATE TABLE PublicationAuthor (id_publ_author INTEGER PRIMARY KEY, id_publ INTEGER REFERENCES Publications (id_publ),
 id_author INTEGER REFERENCES Author (id_author), FOREIGN KEY (id_publ) REFERENCES Publications (id_publ) FOREIGN KEY
  (id_author) REFERENCES Author (id_author));

-- Таблица: PublicationKeywords
DROP TABLE IF EXISTS PublicationKeywords;
CREATE TABLE PublicationKeywords (id_publ_keyword INTEGER PRIMARY KEY, id_publ INTEGER NOT NULL REFERENCES Publications (id_publ), id_keyword INTEGER, FOREIGN KEY (id_publ) REFERENCES Publications (id_publ));

-- Таблица: PublicationLang
DROP TABLE IF EXISTS PublicationLang;
CREATE TABLE PublicationLang (id_publ_lang INTEGER PRIMARY KEY, id_publ INTEGER NOT NULL REFERENCES Publications,
 id_lang INTEGER NOT NULL REFERENCES Lang (id_lang), FOREIGN KEY (id_publ) REFERENCES Publications (id_publ) FOREIGN KEY
  (id_lang) REFERENCES Lang (id_lang));

-- Таблица: Publications
DROP TABLE IF EXISTS Publications;
CREATE TABLE Publications (id_publ INTEGER PRIMARY KEY, id_publ_type INTEGER REFERENCES PublicationType (id_publ_type), publ_name TEXT, abstract TEXT, doi TEXT, id_book INTEGER REFERENCES Book (id_book), year DATE, volume INTEGER, number INTEGER, pages TEXT, FOREIGN KEY (id_publ_type) REFERENCES PublicationType (id_publ_type), FOREIGN KEY (id_book) REFERENCES Book (id_book));

-- Таблица: PublicationType
DROP TABLE IF EXISTS PublicationType;
CREATE TABLE PublicationType (id_publ_type INTEGER PRIMARY KEY, name_type TEXT (50) NOT NULL, dicripsion_type TEXT);

-- Таблица: PublicationUrl
DROP TABLE IF EXISTS PublicationUrl;
CREATE TABLE PublicationUrl (id_url INTEGER PRIMARY KEY, id_publ INTEGER NOT NULL REFERENCES Publications, url TEXT NOT NULL,
 FOREIGN KEY (id_publ) REFERENCES Publications (id_publ));

-- Таблица: Publisher
DROP TABLE IF EXISTS Publisher;
CREATE TABLE Publisher (id_publisher INTEGER PRIMARY KEY, full_name TEXT NOT NULL, short_name TEXT, type TEXT, status TEXT, creation_year INTEGER (4), creation_country INTEGER REFERENCES Country (id_country), parent_company INTEGER, parent_institution TEXT, headquarters TEXT, website TEXT, wiki_url TEXT, predecessor TEXT, owner TEXT, FOREIGN KEY (headquarters) REFERENCES country (id_country));

-- Таблица: PublisherFounders
DROP TABLE IF EXISTS PublisherFounders;
CREATE TABLE PublisherFounders (id_publisher_founder INTEGER PRIMARY KEY, id_publisher INTEGER REFERENCES Publisher (id_publisher), founder_name TEXT);

-- Таблица: PublisherNames
DROP TABLE IF EXISTS PublisherNames;
CREATE TABLE PublisherNames (id_other_name INTEGER PRIMARY KEY, ip_publisher INTEGER REFERENCES Publisher (id_publisher), name TEXT);

-- Таблица: PublisherPublicationsType
DROP TABLE IF EXISTS PublisherPublicationsType;
CREATE TABLE PublisherPublicationsType (id_pp_type INTEGER PRIMARY KEY, id_publisher INTEGER REFERENCES Publisher (id_publisher), pp_type TIME);

-- Представление: All_Publications
DROP VIEW IF EXISTS All_Publications;
CREATE VIEW All_Publications AS SELECT PublicationType.name_type,
       Author.author_name,
       Publications.publ_name,
       Publications.abstract,
       Publications.doi,
       Book.book_name,
       Publications.year,
       Publications.volume,
       Publications.number,
       Publications.pages
  FROM Publications 
  JOIN PublicationType 
  JOIN Book
  JOIN PublicationAuthor
  JOIN Author
  ON Publications.id_publ_type = PublicationType.id_publ_type
  AND Publications.id_book = Book.id_book
  AND Author.id_author = PublicationAuthor.id_author
  AND Publications.id_publ = PublicationAuthor.id_publ;

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
