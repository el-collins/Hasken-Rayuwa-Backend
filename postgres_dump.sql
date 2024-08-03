BEGIN;

-- Create tables
CREATE TABLE IF NOT EXISTS links (
    id CHAR(32) NOT NULL, 
    url VARCHAR NOT NULL, 
    media_type VARCHAR NOT NULL, 
    title VARCHAR, 
    description VARCHAR, 
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS users (
    id CHAR(32) NOT NULL, 
    fullname VARCHAR NOT NULL, 
    email VARCHAR(320) NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS contact (
    id CHAR(32) NOT NULL, 
    fullname VARCHAR NOT NULL, 
    contact_email VARCHAR(320) NOT NULL, 
    message VARCHAR NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS volunteer (
    id CHAR(32) NOT NULL, 
    fullname VARCHAR NOT NULL, 
    volunteer_email VARCHAR(320) NOT NULL, 
    phone_number VARCHAR, 
    address VARCHAR NOT NULL, 
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS state_data (
    id CHAR(32) NOT NULL, 
    "State" VARCHAR(11) NOT NULL, 
    "Lga" VARCHAR NOT NULL, 
    "Ward" VARCHAR NOT NULL, 
    "Village" VARCHAR NOT NULL, 
    "Estimated_Christian_Population" INTEGER NOT NULL, 
    "Estimated_Muslim_Population" INTEGER NOT NULL, 
    "Estimated_Traditional_Religion_Population" INTEGER NOT NULL, 
    "Converts" INTEGER NOT NULL, 
    "Estimated_Total_Population" INTEGER NOT NULL, 
    "Film_Attendance" INTEGER NOT NULL, 
    "People_Group" VARCHAR NOT NULL, 
    "Practiced_Religion" VARCHAR NOT NULL, 
    PRIMARY KEY (id)
);

-- Insert data
INSERT INTO links (id, url, media_type, title, description) VALUES
('a8ea013bbaf743e4a4b5a669723ae318','https://spotifyanchor-web.app.link/e/VxRmKlPyRIb','spotify',NULL,NULL),
('c6254d5a37b94551bfe5edd0d501d259','https://spotifyanchor-web.app.link/e/eRPhQjPyRIb','spotify',NULL,NULL),
('39c7b9bb2684412a9d297a19cb9ad347','https://spotifyanchor-web.app.link/e/OisvWhPyRIb','spotify',NULL,NULL),
('05c7fd6ddd4441fb944554fd2679293e','https://spotifyanchor-web.app.link/e/eli67fPyRIb','spotify',NULL,NULL),
('5c0ad698fe574745916c56298729a3b9','https://spotifyanchor-web.app.link/e/d7CfkePyRIb','spotify',NULL,NULL),
('12ff5b8ed8194af5bea3df434da6adb8','https://spotifyanchor-web.app.link/e/vQnUDbPyRIb','spotify',NULL,NULL),
('b116f6567f5840a29203c3ba67679a16','https://spotifyanchor-web.app.link/e/cXEZj9OyRIb','spotify',NULL,NULL),
('6ebd064b5f5e45cd8d5cbd2728e4d0dc','https://spotifyanchor-web.app.link/e/syFKM6OyRIb','spotify',NULL,NULL),
('f7134f19c4c34ef68992468bfb8cdd1e','https://spotifyanchor-web.app.link/e/aPzUY4OyRIb','spotify',NULL,NULL),
('80dab78e10b54133889c7e1737b3374c','https://spotifyanchor-web.app.link/e/pdw8X1OyRIb','spotify',NULL,NULL),
('f0185e53203e479785f1ad530494c9b4','https://spotifyanchor-web.app.link/e/YvsHQZOyRIb','spotify',NULL,NULL),
('e329ebeca641407db35c7c8c1b4d39b1','https://spotifyanchor-web.app.link/e/tC3rZXOyRIb','spotify',NULL,NULL),
('121b7afdc8d84ebd9957db81af2d57fb','https://spotifyanchor-web.app.link/e/Yh1V9VOyRIb','spotify',NULL,NULL),
('07a16ecf36b741e69b8c12f98a0c868f','https://spotifyanchor-web.app.link/e/zFh9dUOyRIb','spotify',NULL,NULL),
('4974712c12eb4415ab71b30c866e603c','https://spotifyanchor-web.app.link/e/LgEObSOyRIb','spotify',NULL,NULL),
('20712709653a4808bed08ac04f6a3539','https://youtu.be/mLvb9b0iaf8','youtube','It''s Easter Week',NULL),
('7ffb96ad7da040a1b8bd13d9f54e4d81','https://youtu.be/0Wxkg9L_agE','youtube','Pastor  Ibrahim Nathaniel- The son of man',NULL),
('37359055dd4144b6a4a4caf59287bbad','https://youtu.be/zSFhcP4WZ64','youtube','The God''s way of teaching and the God''s way of giving',NULL),
('7ab333105d024421bf2f4bb45d0edf90','https://youtu.be/h4xDebbu1-s','youtube','To the donors, we offer heartfelt gratitude,For your love and support, in magnitude.',NULL),
('e6a27e2509a04979b933e5bf64f5b303','https://youtu.be/9wNCKGiml5I','youtube','My thoughts on Christmas',NULL),
('c8b1d50de3e148ac857a9562a1f0a628','https://youtu.be/Z4oKgKuSqbE','youtube','General Thanksgiving (HRAM) 2023',NULL),
('d65a96d4ad4b48859a5c9b5ebe6af4d8','https://youtu.be/XJLWldMbYPA','youtube','A Heartfelt Thank',NULL),
('28d2f589e19547afb41c74e76e62fe64','https://youtu.be/O5gXlocx6UU','youtube','Gratitude By Go Team Leader',NULL),
('b5f91a6f1f014e3fbfd02353606e3796','https://youtu.be/iAHXd5PFOAs','youtube','YAN GUDUN HIJIRA Refugees  a Daki Takwas story',NULL);

INSERT INTO state_data (id, "State", "Lga", "Ward", "Village", "Estimated_Christian_Population", "Estimated_Muslim_Population", "Estimated_Traditional_Religion_Population", "Converts", "Estimated_Total_Population", "Film_Attendance", "People_Group", "Practiced_Religion") VALUES
('9f1d6f3a537e4dc8b69649f3d627b14b','Sokoto','Binji','Maikulki','Maikulki',0,6000,0,0,6000,1125,'Hausa/Fulani','Islam'),
('2ad6771c41f042719c8b479356544cef','Sokoto','Binji','Bunkari','Bunkari',0,2500,0,0,2500,764,'Hausa/Fulani','Islam'),
('01f47b08bd2748b0a76c60aec9f40e68','Sokoto','Silame','Gande East ','Garin magaji ',0,3500,0,0,3500,240,'Hausa/Fulani','Islam'),
('e2d21693bb4549349c4186c9ae5f9299','Sokoto','Silame','Gande','Gande',0,4000,0,0,4000,964,'Hausa/Fulani','Islam'),
('907c6874c29d4da4a08d6f64ad0c8786','Sokoto','Silame','Silame','Dankala',0,2000,0,0,2000,255,'Hausa/Fulani','Islam'),
('8698a73b895a481498dbc115df05bc3e','Sokoto','Silame','Silame','Runji',0,5000,0,0,5000,649,'Hausa/Fulani','Islam'),
('749f5c711f9c423b99500d2791c28646','Sokoto','GADA ','Gada','Engaboro ',0,5000,0,0,5000,245,'Hausa/Fulani','Islam'),
('77f21b182a544aa08d4b71ed169faf6c','Sokoto','Gada','Gada','Sabon Gari',0,6000,0,0,6000,126,'Hausa/Fulani','Islam'),
('31ec0bc19fa540cdba013307ad0abe2c','Sokoto','Gada','Kiri','Gidan dabo',0,3000,0,0,3000,487,'Hausa/Fulani','Islam'),
('d0a0197ea7dd40c7a50a5ad2508dd388','Sokoto','Gada','Kiri','Shiyar magaji',0,1500,0,0,1500,389,'Hausa/Fulani','Islam'),
('e2d4ce95de8b4b569b5562ae671160c9','Sokoto','Gada','Kiri','Gadassaka',0,1200,0,0,1200,130,'Hausa/Fulani','Islam'),
('bfe7de057672432fb9acb756f0057e57','Sokoto','Wammako ','Wammako ','Gidan Dankaiwo',0,2000,0,0,2000,516,'Hausa/Fulani','Islam'),
('e98bf4d20bd64e3ba6098507692d6d8e','Sokoto','Wammako ','kaura/Gedawa','Runjin biyo',0,2000,0,0,2000,354,'Hausa/Fulani','Islam'),
('743c9b6cd9d3411e9e21121dafc7b486','Sokoto','Wammako ','Wammako ','Wajeka',0,3000,0,0,3000,745,'Hausa/Fulani','Islam'),
('f6f5cec1ea7e49eca02dffa31194984c','Sokoto','Isa','Isa North','Isa',15,8000,0,12,8015,1500,'Hausa/Fulani','Islam'),
('dc1cce3668334db09ea1b3c738c00260','Sokoto','Bodinga','modorawa','takatuku',0,1250,0,0,1250,356,'Hausa/Fulani','Islam'),
('c70b36abfb464b238077c380522cbae0','Sokoto','Shagari','Gangam','Tungan Mamu',0,1500,0,12,1500,120,'Hausa/Fulani','Islam');

-- Create indexes
CREATE UNIQUE INDEX IF NOT EXISTS ix_links_url ON links (url);
CREATE INDEX IF NOT EXISTS ix_links_media_type ON links (media_type);
CREATE INDEX IF NOT EXISTS "ix_state_data_Lga" ON state_data ("Lga");

COMMIT;