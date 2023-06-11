### **CroMa Real-Time Database Rules**

```
{
  "rules": {
      // Only admins are allowed to CRUD data values
      "users": {
            ".write": "auth != null && root.child('admins').hasChild(auth.uid)", // Defines write access
            ".read": "auth != null && root.child('admins').hasChild(auth.uid)", // Defines read access
      }
  }
}
```
