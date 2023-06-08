DROP TABLE IF EXISTS Watches CASCADE;

CREATE TABLE IF NOT EXISTS Watches
(
    id serial unique not null PRIMARY KEY,
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
    "Complication" character varying(40),
    "Power Reserve" character varying(40),
    price character varying(40)
)

DELETE FROM Watches


CREATE INDEX IF NOT EXISTS watches_index
ON Watches (brand, model, "Case Material", "Strap Material",
"Movement Type", "Water Resistance", "Case Diameter","Case Thickness",
"Band Width", "Dial Color", "Crystal Material", "Comlication", "Power Reserve");


