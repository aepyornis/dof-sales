drop table if exists dof_sales;

create table dof_sales (
  Borough char(1),
  Neighborhood text,
  BuildingClassCategory text,
  TaxClassAtPresent text,
  Block char(5),
  Lot char(4),
  EaseMent text,
  BuildingClassAtPresent text,
  Address text,
  ApartmentNumber text,
  ZipCode char(5),
  ResidentialUnits integer,
  CommercialUnits integer,
  TotalUnits integer,
  LandSquareFeet integer,
  GrossSquareFeet integer,
  YearBuilt integer,
  TaxClassAtTimeOfSale text,
  BuildingClassAtTimeOfSale text,
  SalePrice bigint,
  SaleDate date,
  bbl char(10),
  id serial PRIMARY KEY
);
