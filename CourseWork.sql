CREATE TABLE Users (
  UserID Serial PRIMARY KEY ,
  Username VARCHAR(255) UNIQUE NOT NULL,
  Password VARCHAR(255) NOT NULL,
  Email VARCHAR(255) UNIQUE NOT NULL,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL
);
alter table Users add constraint email_unique unique(Email)
CREATE TABLE Product (
  ProductID Serial PRIMARY KEY ,
  Name VARCHAR(255) NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  BrandID INT NOT NULL,
  CategoryID INT NOT NULL,
  Material VARCHAR(255) NOT NULL,
  Condition VARCHAR(255) NOT NULL,
  ProductArticle text unique not null,
  FOREIGN KEY (BrandID) REFERENCES Brand (BrandID),
  FOREIGN KEY (CategoryID) REFERENCES Category (CategoryID)
);

CREATE TABLE Brand (
  BrandID Serial PRIMARY KEY ,
  Name VARCHAR(255) unique NOT NULL
);
CREATE TABLE Category (
  CategoryID Serial PRIMARY KEY,
  Name VARCHAR(255) unique NOT NULL
);
CREATE TABLE Cart (
  CartID Serial PRIMARY KEY ,
  UserID INT NOT NULL,
  ProductID int not null,
  Quantity int,
  FOREIGN KEY (UserID) REFERENCES Users (UserID),
  FOREIGN KEY (ProductID) REFERENCES Product (ProductID)
);
CREATE TABLE "Order" (
  OrderID Serial PRIMARY KEY ,
  UserID INT NOT NULL,
  OrderDate Timestamp NOT NULL,
  ShippingAddress VARCHAR(255) NOT NULL,
  BillingAddress VARCHAR(255) NOT NULL,
  PaymentMethod VARCHAR(255) NOT NULL,
  FOREIGN KEY (UserID) REFERENCES Users (UserID)
);

alter table "Order" add column Status  VARCHAR(255) not null;
CREATE TABLE Order_Item (
  OrderItemID Serial PRIMARY KEY ,
  OrderID INT NOT NULL,
  ProductID INT NOT NULL,
  Quantity INT NOT NULL,
  FOREIGN KEY (OrderID) REFERENCES "Order" (OrderID),
  FOREIGN KEY (ProductID) REFERENCES Product (ProductID)
);
CREATE TABLE Wishlist (
  WishlistID Serial PRIMARY KEY ,
  UserID INT NOT NULL,
  ProductID INT NOT NULL,
  FOREIGN KEY (UserID) REFERENCES Users (UserID),
  FOREIGN KEY (ProductID) REFERENCES Product (ProductID)
);

CREATE UNIQUE INDEX Wishlist_unique
ON Wishlist (UserID, ProductID);

CREATE UNIQUE INDEX Cart_unique
ON Cart (UserID, ProductID);

CREATE UNIQUE INDEX Order_Item_unique
ON Order_Item (OrderID, ProductID);

SElECT * FROM product

SElECT * FROM users

SElECT * FROM wishlist

SElECT * FROM Cart

SElECT * FROM Order_Item

SElECT * FROM "Order"
