# https://dbdiagram.io

Table User {
  id bigint [pk, increment]
  username varchar
  email email
  password varchar
  first_name varchar
  last_name varchar
  is_active bool
  is_staff bool
  is_superuser bool
  date_joined datetime
  last_login datetime
}

Table Product {
  id bigint [pk, increment]
  name varchar
  description text
  image file
  price decimal
  stock int
}

Table Order {
  order_id uuid [pk]
  user bigint 
  created_at datetime
  status varchar
}

Table OrderItem {
  id bigint [pk, increment]
  order uuid 
  product bigint 
  quantity int
}


Ref: "OrderItem"."product" < "Product"."id"

Ref: "OrderItem"."order" < "Order"."order_id"

Ref: "User"."id" < "Order"."user"