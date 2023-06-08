DROP TABLE IF EXISTS Watches CASCADE;

CREATE TABLE IF NOT EXISTS Watches
(
    pk serial unique not null PRIMARY KEY,
    brand character varying(40),
    model character varying(40),
    "Case Material" character varying(40),
    "Strap Material" character varying(40),
    "Movement Type" character varying(40),
    "Water Resistance" character varying(40),
    "Case Diameter" character varying(40),
    "Case Thickness" character varying(40),
    "Band Width" character varying(40),
    "Dial Color" character varying(40),
    "Crystal Material" character varying(40),
    "Complications" character varying(40),
    "Power Reserve" character varying(40),
    price character varying(40)
);

DELETE FROM Watches;


CREATE INDEX IF NOT EXISTS watches_index
ON Watches (brand, model, "Case Material", "Strap Material",
"Movement Type", "Water Resistance", "Case Diameter","Case Thickness",
"Band Width", "Dial Color", "Crystal Material", "Complications", "Power Reserve");

CREATE TABLE IF NOT EXISTS Sell(
    brandrep_pk int not null REFERENCES BrandRep(pk) ON DELETE CASCADE,
    watches_pk int not null REFERENCES Watches(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (brandrep_pk, watches_pk)
);

DELETE FROM Sell;

DROP TABLE IF EXISTS WatchOrder;

CREATE TABLE IF NOT EXISTS WatchOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    brandrep_pk int not null REFERENCES BrandRep(pk) ON DELETE CASCADE,
    watches_pk int not null REFERENCES Watches(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM WatchOrder;

CREATE OR REPLACE VIEW vw_watches
AS
SELECT p.brand, p.model, p."Case Material",
       p."Strap Material", p."Movement Type", p."Water Resistance", 
       p."Case Diameter", p."Case Thickness", p."Band Width", p."Dial Color",
       p."Crystal Material", p."Complications", p."Power Reserve" ,p.price,
       p.pk as watches_pk,
       f.full_name as brandrep_name,
       f.pk as brandrep_pk
FROM Watches p
JOIN Sell s ON s.watches_pk = p.pk
JOIN BrandRep f ON s.brandrep_pk = f.pk
ORDER BY available, p.pk;

