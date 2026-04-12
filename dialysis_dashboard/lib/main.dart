import 'dart:async';
import 'dart:convert';
import 'dart:html'; // WebSocket for Flutter Web
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

  final String baseUrl = "http://localhost:5001/";
  WebSocket? socket;

  final nameCtrl = TextEditingController();
  final ageCtrl = TextEditingController();
  final genderCtrl = TextEditingController();
  final hoursCtrl = TextEditingController(text: "4");

  @override
  void initState() {
    super.initState();
    fetchData();
    connectSocket();

    // ✅ Keep API for time + alerts
    timer = Timer.periodic(
      const Duration(seconds: 1),
      (_) => fetchData(),
    );
  }

  @override
  void dispose() {
    timer?.cancel();
    socket?.close();
    nameCtrl.dispose();
    ageCtrl.dispose();
    genderCtrl.dispose();
    hoursCtrl.dispose();
    super.dispose();
  }

  // ================= SOCKET =================
  void connectSocket() {
    socket = WebSocket('ws://localhost:8080');

    socket!.onMessage.listen((event) {
      if (data == null) return;

      // ❌ BLOCK if no patient
      if (data!['patient'] == null) return;

      String state = data!['system_state'].toString();

      // ❌ BLOCK if system not active
      if (state != "RUNNING" &&
          state != "STABILISATION" &&
          state != "EMERGENCY_STOP") return;

      var parts = event.data.split(',');

      setState(() {
        double vib = double.parse(parts[1]);

        data!['vibration'] = vib.toStringAsFixed(4);

        // dynamic pressure
        data!['arterial_pressure'] =
            (160 + vib * 200).toStringAsFixed(1);
        data!['venous_pressure'] =
            (180 + vib * 200).toStringAsFixed(1);
      });
    });
  }

  // ================= FETCH DATA =================
  Future<void> fetchData() async {
    try {
      final res = await http.get(Uri.parse("${baseUrl}data"));

      if (res.statusCode == 200) {
        final newData = jsonDecode(res.body);

        setState(() {
          data ??= {};

          // 🔥 preserve Arduino values
          final vibration = data!['vibration'];
          final arterial = data!['arterial_pressure'];
          final venous = data!['venous_pressure'];

          data = newData;

          // 🔥 restore live values
          data!['vibration'] = vibration ?? newData['vibration'];
          data!['arterial_pressure'] =
              arterial ?? newData['arterial_pressure'];
          data!['venous_pressure'] =
              venous ?? newData['venous_pressure'];
        });
      }
    } catch (_) {}
  }

  // ================= PATIENT =================
  Future<void> registerPatient() async {
    try {
      final response = await http.post(
        Uri.parse("${baseUrl}patients"),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "name": nameCtrl.text,
          "age": int.tryParse(ageCtrl.text) ?? 0,
          "gender": genderCtrl.text,
          "hours": int.tryParse(hoursCtrl.text) ?? 4,
        }),
      );

      if (response.statusCode == 200) {
        await fetchData();
        Navigator.pop(context);
      }
    } catch (e) {
      print(e);
    }
  }

  Future<void> startSystem() async {
    await http.post(Uri.parse("${baseUrl}start"));
    await Future.delayed(const Duration(milliseconds: 300));
    await fetchData();
  }

  Future<void> stopSystem() async {
    await http.post(Uri.parse("${baseUrl}stop"));

    setState(() {
      data!['vibration'] = "--";
      data!['arterial_pressure'] = "--";
      data!['venous_pressure'] = "--";
    });

    await fetchData();
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

    if (state == "EMERGENCY_STOP") {
      bg = Colors.red.shade900;
    } else if (state == "STABILISATION") {
      bg = Colors.orange.shade900;
    } else if (state == "RUNNING") {
      bg = Colors.green.shade900;
    }

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

            Text(
              state,
              style: const TextStyle(
                fontSize: 26,
                fontWeight: FontWeight.bold,
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
            TextField(
                controller: nameCtrl,
                decoration: const InputDecoration(labelText: "Name")),
            TextField(
                controller: ageCtrl,
                decoration: const InputDecoration(labelText: "Age")),
            TextField(
                controller: genderCtrl,
                decoration: const InputDecoration(labelText: "Gender")),
            TextField(
                controller: hoursCtrl,
                decoration:
                    const InputDecoration(labelText: "Dialysis Hours")),
          ],
        ),
        actions: [
          TextButton(
              onPressed: registerPatient,
              child: const Text("SAVE")),
        ],
      ),
    );
  }
}