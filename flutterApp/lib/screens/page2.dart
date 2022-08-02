import 'package:flutter/material.dart';
import 'package:timeline_tile/timeline_tile.dart';

class Page4 extends StatelessWidget {
  const Page4({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Kollam  Superfast Bus'),
      ),
      body: Column(children: [
        Column(children: [
          Container(
              child: Row(children: [
            Text('Destination: palayam'),
            Spacer(),
            Text('alert')
          ])),
        ]),
        Container(
          margin: EdgeInsets.only(top: 30),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              SizedBox(
                child: TimelineTile(
                  indicatorStyle: IndicatorStyle(
                    color: Colors.green,
                  ),
                  afterLineStyle: LineStyle(color: Colors.green),
                  alignment: TimelineAlign.start,
                  endChild: Container(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Text("15.30"),
                        Padding(
                          padding: const EdgeInsets.only(top: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('kollam Central'),
                              Text('on Time.Departed from kollam'),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                  isFirst: true,
                ),
              ),
              SizedBox(
                child: TimelineTile(
                  indicatorStyle: IndicatorStyle(color: Colors.green),
                  beforeLineStyle: LineStyle(color: Colors.green),
                  afterLineStyle: LineStyle(color: Colors.green),
                  alignment: TimelineAlign.start,
                  endChild: Container(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Text("15.30"),
                        Padding(
                          padding: const EdgeInsets.only(top: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('kollam Central'),
                              Text('on Time.Departed from kollam'),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              ),
              SizedBox(
                child: TimelineTile(
                  indicatorStyle: IndicatorStyle(color: Colors.green),
                  beforeLineStyle: LineStyle(color: Colors.green),
                  afterLineStyle: LineStyle(color: Colors.green),
                  alignment: TimelineAlign.start,
                  endChild: Container(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Text("15.30"),
                        Padding(
                          padding: const EdgeInsets.only(top: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('kollam Central'),
                              Text('on Time.Departed from kollam'),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              ),
              SizedBox(
                child: TimelineTile(
                  indicatorStyle: IndicatorStyle(color: Colors.green),
                  beforeLineStyle: LineStyle(color: Colors.green),
                  afterLineStyle: LineStyle(color: Colors.green),
                  alignment: TimelineAlign.start,
                  endChild: Container(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Text("15.30"),
                        Padding(
                          padding: const EdgeInsets.only(top: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('kollam Central'),
                              Text('on Time.Departed from kollam'),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              ),
              SizedBox(
                child: TimelineTile(
                  indicatorStyle:
                      IndicatorStyle(color: Colors.green, height: 30),
                  beforeLineStyle: LineStyle(color: Colors.green),
                  afterLineStyle: LineStyle(color: Colors.green),
                  alignment: TimelineAlign.start,
                  endChild: Container(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Text("15.30"),
                        Padding(
                          padding: const EdgeInsets.only(top: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('kollam Central'),
                              Text('on Time.Departed from kollam'),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              ),
              SizedBox(
                child: TimelineTile(
                  indicatorStyle: IndicatorStyle(color: Colors.red),
                  beforeLineStyle: LineStyle(color: Colors.green),
                  alignment: TimelineAlign.start,
                  endChild: Container(
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Text("15.30"),
                        Padding(
                          padding: const EdgeInsets.only(top: 10),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Text('kollam Central'),
                              Text('on Time.Departed from kollam'),
                            ],
                          ),
                        )
                      ],
                    ),
                  ),
                  isLast: true,
                ),
              ),
            ],
          ),
        ),
      ]),
    );
  }
}
