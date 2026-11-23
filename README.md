# Address Detection API

## Detail 
 first intern 2 month project
 Detect Address from Text
 program find province, amphoe, district, zipcode, name, phone

## Program Process 
 Program INPUT <= 
 ``` 
  {
    "text": "อนงค์ลักษณ์\n9/56 ม.3\nหมู่บ้านนฤมลศิริ(ซอย2)\nซ.บุญศิริ ถ.สุขุมวิท\nต.บางเมือง\nอ.เมืองสมุทรปราการ\nจ.สมุทรปนาการ\n10270\nโทร.0956029655"
  }  
 ```

 Program PROCESS 
 ``` 
 get text -> tokenize -> spellcheck -> matching
  *custom tokenize and spellcheck base on Dict Tire 
  **matching find address province amphoe tambol base on address_list file 
 ```  
 Program OUTPUT =>
 ``` 
  {
    "address": {
      "province": "สมุทรปราการ",
      "amphoe": "เมืองสมุทรปราการ",
      "district": "บางเมือง",
      "zipcode": "10270",
      "name": "",
      "phone": "0956029655"
    }
  }  
 ```

## Build Docker
 ``` 
 docker build -t address-api:v1 .
 docker run -p 8000:8000 --name address-service address-api:v1 
 ```
 or
 ``` 
 docker compose up 
 ```  

## How to use
 1. before run program
 2. go to 127.0.0.1/docs
 3. POST box /address-check
    sent Request body format
    { "text": "Enter address text" }
 4. Execute btn

