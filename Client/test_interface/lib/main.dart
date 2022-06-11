import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

Future<Album> fetchAlbum() async {
  final response = await http.get(Uri.parse('http://localhost:5000/youngs/'));

  if (response.statusCode == 200) {
    // All good from the server, parse the JSON
    return Album.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to retrieve drink');
  }
}

class Album {
  final String name;
  final String description;

  const Album({required this.name, required this.description});

  factory Album.fromJson(Map<String, dynamic> json) {
    return Album(
      name: json['name'],
      description: json['description'],
    );
  }
}

void main() => runApp(const MyApp());

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  late Future<Album> futureAlbum;

  @override
  void initState() {
    super.initState();
    futureAlbum = fetchAlbum();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fetch Data Example',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Fetch Data Example'),
        ),
        body: Center(
          child: FutureBuilder<Album>(
            future: futureAlbum,
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                return Text("Drink:           " +
                    snapshot.data!.name +
                    "\nDescription: " +
                    snapshot.data!.description);
              } else if (snapshot.hasError) {
                return Text('${snapshot.error}');
              }

              // By default, show a loading spinner.
              return const CircularProgressIndicator();
            },
          ),
        ),
      ),
    );
  }
}
