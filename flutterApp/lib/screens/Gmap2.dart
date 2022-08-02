import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:sample__pro1/screens/page2.dart';

class MapSample2 extends StatelessWidget {
  const MapSample2({Key? key}) : super(key: key);

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
                    'SHOWING BUSES TO UCK',
                  ),
                ),
                Column(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [],
                ),
                Row(children: [
                  Icon(IconData(0xe1d5, fontFamily: 'MaterialIcons')),
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
              builder: (context) => Page4(),
            ),
          );
        },
        child: Icon(Icons.pin_drop_outlined),
      ),
    );
  }
}
