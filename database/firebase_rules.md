### **CroMa Real-Time Database**
```
{
  "rules": {
      //only admins are allowed to CRUD data values
      "users": {
            ".write": "auth != null && root.child('admins').hasChild(auth.uid)",
            ".read": "auth != null && root.child('admins').hasChild(auth.uid)",
      }
  }
}
```
