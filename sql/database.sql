
CREATE TABLE public.titles (
    id VARCHAR(255) PRIMARY KEY,
    runningTimeInMinutes INTEGER,
    nextEpisode VARCHAR(255),
    numberOfEpisodes INTEGER,
    seriesEndYear INTEGER,
    seriesStartYear INTEGER,
    title VARCHAR(255),
    titleType VARCHAR(255),
    year INTEGER
);



CREATE TABLE public.images (
    id VARCHAR(255) PRIMARY KEY,
    title_id VARCHAR(255) REFERENCES titles(id),
    height INTEGER,
    url TEXT,
    width INTEGER
);

CREATE TABLE public.principals (
    id VARCHAR(255) PRIMARY KEY,
    title_id VARCHAR(255) REFERENCES titles(id),
    legacyNameText TEXT,
    name VARCHAR(255),
    category VARCHAR(255),
    endYear INTEGER,
    episodeCount INTEGER,
    startYear INTEGER
);

CREATE TABLE public.roles (
    principal_id VARCHAR(255) REFERENCES principals(id),
    character VARCHAR(255),
    characterId VARCHAR(255)
);
