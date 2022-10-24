### **CroMa Real-Time Database**
```
{
  "rules": {

      "users": {
            ".write": "auth != null && root.child('admins').hasChild(auth.uid)",
            ".read": "auth != null && root.child('admins').hasChild(auth.uid)",
      }
  }
}
```
