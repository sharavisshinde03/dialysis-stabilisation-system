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
      theme: ThemeData.dark(),
      home: const Dashboard(),
    );
  }
}

class Dashboard extends StatefulWidget {
  const Dashboard({super.key});

  @override
  State<Dashboard> createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  Map<String, dynamic>? data;
  Timer? timer;

  final String baseUrl = "http://localhost:5001";

  final nameCtrl = TextEditingController();
  final ageCtrl = TextEditingController();
  final genderCtrl = TextEditingController();
  final hoursCtrl = TextEditingController(text: "4");

  @override
  void initState() {
    super.initState();
    fetchData();
    timer = Timer.periodic(const Duration(seconds: 1), (_) => fetchData());
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  // ================= API =================

  Future<void> fetchData() async {
    try {
      final res = await http.get(Uri.parse("$baseUrl/data"));
      if (res.statusCode == 200) {
        setState(() {
          data = jsonDecode(res.body);
        });
      }
    } catch (_) {
      setState(() {
        data = {
          "system_state": "DISCONNECTED",
          "alerts": [],
          "patient": null,
          "blood_flow": "--",
          "arterial_pressure": "--",
          "venous_pressure": "--",
          "vibration": "--",
          "remaining_time": "--:--:--",
        };
      });
    }
  }

  Future<void> submitPatient() async {
    await http.post(
      Uri.parse("$baseUrl/set_patient"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "name": nameCtrl.text,
        "age": int.tryParse(ageCtrl.text) ?? 0,
        "gender": genderCtrl.text,
        "hours": int.tryParse(hoursCtrl.text) ?? 4,
      }),
    );

    Navigator.pop(context);
  }

  Future<void> startSystem() async {
    await http.post(Uri.parse("$baseUrl/start"));
  }

  Future<void> stopSystem() async {
    await http.post(Uri.parse("$baseUrl/stop"));
  }

  // ================= UI =================

  @override
  Widget build(BuildContext context) {
    if (data == null) {
      return const Scaffold(
        body: Center(child: Text("Connecting to server...")),
      );
    }

    final state = data!['system_state'];
    final alerts = data!['alerts'] as List;

    Color bg = Colors.black;
    if (state == "EMERGENCY_STOP") bg = Colors.red.shade900;
    if (state == "STABILISATION") bg = Colors.orange.shade900;
    if (state == "RUNNING") bg = Colors.green.shade900;

    return Scaffold(
      backgroundColor: bg,
      appBar: AppBar(
        title: const Text("AI Dialysis Dashboard"),
        actions: [
          TextButton(
            onPressed: showPatientDialog,
            child: const Text("Add Patient",
                style: TextStyle(color: Colors.white)),
          ),
          TextButton(
            onPressed: startSystem,
            child: const Text("Start",
                style: TextStyle(color: Colors.greenAccent)),
          ),
          TextButton(
            onPressed: stopSystem,
            child: const Text("Stop",
                style: TextStyle(color: Colors.redAccent)),
          ),
          const SizedBox(width: 16),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: ListTile(
                title: Text(data!['patient']?['name'] ?? "No Patient"),
                subtitle: Text(
                  "Age: ${data!['patient']?['age'] ?? '--'} | "
                  "Gender: ${data!['patient']?['gender'] ?? '--'}",
                ),
              ),
            ),
            const SizedBox(height: 12),

            Wrap(
              spacing: 12,
              runSpacing: 12,
              children: [
                stat("Blood Flow", "${data!['blood_flow']} ml/min"),
                stat("Arterial", "${data!['arterial_pressure']} mmHg"),
                stat("Venous", "${data!['venous_pressure']} mmHg"),
                stat("Vibration", "${data!['vibration']} g"),
                stat("Time Left", data!['remaining_time']),
                stat("State", state),
              ],
            ),

            const SizedBox(height: 16),
            const Text("Alerts", style: TextStyle(fontSize: 18)),
            Expanded(
              child: alerts.isEmpty
                  ? const Center(child: Text("No alerts"))
                  : ListView.builder(
                      itemCount: alerts.length,
                      itemBuilder: (_, i) => ListTile(
                        leading: const Icon(Icons.warning,
                            color: Colors.redAccent),
                        title: Text(alerts[i]['message']),
                        subtitle: Text(alerts[i]['time']),
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget stat(String title, String value) {
    return Container(
      width: 170,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.grey.shade900,
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: Colors.grey.shade700),
      ),
      child: Column(
        children: [
          Text(title),
          const SizedBox(height: 6),
          Text(value,
              style:
                  const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  void showPatientDialog() {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text("Set Patient"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(controller: nameCtrl, decoration: const InputDecoration(labelText: "Name")),
            TextField(controller: ageCtrl, decoration: const InputDecoration(labelText: "Age")),
            TextField(controller: genderCtrl, decoration: const InputDecoration(labelText: "Gender")),
            TextField(controller: hoursCtrl, decoration: const InputDecoration(labelText: "Dialysis Hours")),
          ],
        ),
        actions: [
          TextButton(onPressed: submitPatient, child: const Text("SAVE")),
        ],
      ),
    );
  }
}
