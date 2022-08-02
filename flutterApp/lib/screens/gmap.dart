import 'dart:async';
import 'dart:convert';
import 'dart:ui';

import 'package:flutter/src/foundation/key.dart';
import 'package:flutter/src/widgets/framework.dart';

import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:sample__pro1/screens/Gmap2.dart';

class MapSample extends StatelessWidget {
  const MapSample({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Google map"),
      ),
      body: Stack(children: [
        GoogleMap(
          initialCameraPosition: CameraPosition(
              target: LatLng(22.5448131, 88.34444444691), zoom: 15),
        ),
        Align(
          alignment: Alignment.bottomCenter,
          child: Container(
            decoration: BoxDecoration(
                color: Colors.white,
                border: Border.all(width: 3, color: Colors.blue),
                borderRadius: BorderRadius.all(Radius.circular(10)),
                boxShadow: [
                  BoxShadow(
                      blurRadius: 5, offset: Offset(8, 4), color: Colors.grey)
                ]),
            margin: EdgeInsets.only(bottom: 20),
            width: 300,
            height: 150,
            padding: EdgeInsets.only(bottom: 10),
            alignment: Alignment.bottomCenter,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Container(
                  padding: EdgeInsets.only(top: 8),
                  child: Text(
                    'SHOWING BUSES TO PALAYAM',
                  ),
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Icon(IconData(0xe1d5, fontFamily: 'MaterialIcons')),
                    Text('Buses every 8 minutes'),
                    Icon(IconData(0xe038, fontFamily: 'MaterialIcons')),
                    Text('1 hr 8 min'),
                  ],
                ),
                Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Text('Expected fare RS 124 .Light Rush'),
                      Text('Nearest superfast bus arriving in 30 min')
                    ]),
              ],
            ),
          ),
        ),
      ]),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => MapSample2(),
            ),
          );
        },
        child: Icon(Icons.pin_drop_outlined),
      ),
    );
  }
}
