import 'package:flutter/material.dart';
import 'package:sample__pro1/screens/gmap.dart';
import 'package:sample__pro1/screens/page2.dart';
import 'package:timeline_tile/timeline_tile.dart';

class Page1 extends StatelessWidget {
  const Page1({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Page 1'),
        ),
        body: Container(
          width: MediaQuery.of(context).size.width,
          height: MediaQuery.of(context).size.height,
          color: Colors.blue,
          child: Stack(children: [
            Container(
              margin: EdgeInsets.all(100),
              width: 400,
              height: 200,
              decoration: BoxDecoration(
                  image: DecorationImage(
                      image: AssetImage('logo.jpg'), fit: BoxFit.contain),
                  borderRadius: BorderRadius.all(Radius.circular(5))),
            ),
            Column(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                ElevatedButton(
                    onPressed: () {
                      Navigator.push(context,
                          MaterialPageRoute(builder: (context) => MapSample()));
                    },
                    child: Text('next page')),
              ],
            )
          ]),
        ));
  }
}
