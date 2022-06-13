import 'dart:convert';
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