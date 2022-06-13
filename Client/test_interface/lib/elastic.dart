import 'package:http/http.dart' as http;

Future<HBBdouble> fetchValue(String lib, String function, List<String> args) async {
  final response;
  String url = 'https://localhost:5000/' + lib + '/' + function + '/'
  for(int i = 0; i < args.length; i++)
  {
    url += args[i] + '/';
  }

  response = await http.get(Uri.parse(url));

  if (response.statusCode == 200) {
    // All good from the server, parse the JSON
    return Album.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to retrieve value');
  }
}

class HBBdouble {
  final double value

  const Album({required this.value});

  factory Album.fromJson(Map<String, dynamic> json) {
    return Album(
      value: json['value'],
    );
  }
}