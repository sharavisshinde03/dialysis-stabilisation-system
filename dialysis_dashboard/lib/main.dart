import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const DialysisApp());
}

class DialysisApp extends StatelessWidget {
  const DialysisApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Dialysis Dashboard',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF121212),
        cardColor: const Color(0xFF1E1E1E),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF1F6FEB),
        ),
      ),
      home: const DashboardPage(),
    );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  Map<String, dynamic>? data;
  bool loading = true;
  Timer? timer;

  @override
  void initState() {
    super.initState();
    fetchData();
    timer = Timer.periodic(
      const Duration(seconds: 1),
      (_) => fetchData(),
    );
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  Future<void> fetchData() async {
    try {
      final res =
          await http.get(Uri.parse("http://127.0.0.1:5000/data"));

      if (res.statusCode == 200) {
        setState(() {
          data = jsonDecode(res.body);
          loading = false;
        });
      }
    } catch (e) {
      debugPrint("ERROR: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final state = data!['system_state'];
    final alerts = data!['alerts'] as List;

    return Scaffold(
      appBar: AppBar(
        title: const Text("AI Dialysis Monitoring Dashboard"),
        backgroundColor:
            state == "EMERGENCY_STOP" ? Colors.red : Colors.blue,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: ListTile(
                title: Text(
                  data!['patient']?['name'] ?? "No Patient Selected",
                ),
                subtitle: Text(
                  "Age: ${data!['patient']?['age'] ?? '--'} | "
                  "Gender: ${data!['patient']?['gender'] ?? '--'}",
                ),
              ),
            ),

            const SizedBox(height: 16),

            GridView.count(
              shrinkWrap: true,
              crossAxisCount: 3,
              childAspectRatio: 2.5,
              children: [
                vitalsCard("Blood Flow", "${data!['blood_flow']} ml/min"),
                vitalsCard("Arterial Pressure",
                    "${data!['arterial_pressure']} mmHg"),
                vitalsCard("Venous Pressure",
                    "${data!['venous_pressure']} mmHg"),
                vitalsCard("Vibration", "${data!['vibration']} g"),
                vitalsCard("Remaining Time",
                    data!['remaining_time'] ?? "--"),
                vitalsCard("System State", state),
              ],
            ),

            const SizedBox(height: 20),

            const Text(
              "Alert Log",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),

            Expanded(
              child: ListView.builder(
                itemCount: alerts.length,
                itemBuilder: (context, index) {
                  return ListTile(
                    leading:
                        const Icon(Icons.warning, color: Colors.red),
                    title: Text(alerts[index]['message']),
                    subtitle: Text(alerts[index]['time']),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget vitalsCard(String title, String value) {
    return Card(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(title,
                style: const TextStyle(
                    fontSize: 14, fontWeight: FontWeight.bold)),
            const SizedBox(height: 4),
            Text(value, style: const TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
