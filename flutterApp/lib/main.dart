import 'package:flutter/material.dart';
import 'package:sample__pro1/screens/page1.dart';
import './screens/Gmap2.dart';
import 'package:sample__pro1/screens/gmap.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        title: 'login',
        theme: ThemeData(primarySwatch: Colors.blue),
        home: homepage());
  }
}

class homepage extends StatelessWidget {
  const homepage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Home screen"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Click the icon',
              style: TextStyle(fontSize: 24),
            )
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => Page1(),
            ),
          );
        },
        child: Icon(Icons.pin_drop_outlined),
      ),
    );
  }
}
