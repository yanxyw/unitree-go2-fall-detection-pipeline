import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:http/http.dart' as http;

final FlutterLocalNotificationsPlugin
    flutterLocalNotificationsPlugin =
    FlutterLocalNotificationsPlugin();

Future<void> _firebaseMessagingBackgroundHandler(
    RemoteMessage message) async {
  await Firebase.initializeApp();
  print(
      "📩 Background Message: ${message.notification?.title} - ${message.notification?.body}");
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  /// ✅ Set background message handler
  FirebaseMessaging.onBackgroundMessage(
      _firebaseMessagingBackgroundHandler);

  /// ✅ Initialize Local Notifications
  const AndroidInitializationSettings
      androidInitializationSettings =
      AndroidInitializationSettings('@mipmap/ic_launcher');
  const DarwinInitializationSettings
      iosInitializationSettings =
      DarwinInitializationSettings();
  const InitializationSettings initializationSettings =
      InitializationSettings(
    android: androidInitializationSettings,
    iOS: iosInitializationSettings,
  );

  await flutterLocalNotificationsPlugin
      .initialize(initializationSettings);

  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'FCM Demo',
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? _fcmToken;

  @override
  void initState() {
    super.initState();
    _fetchFcmToken();
    _setupFCMListeners();
  }

  /// ✅ Get FCM Token
  Future<void> _fetchFcmToken() async {
  try {
    String? token = await FirebaseMessaging.instance.getToken();
    print("✅ FCM Token: $token");

    if (token != null) {
      setState(() {
        _fcmToken = token;
      });

      final response = await http.post(
        Uri.parse('http://10.0.2.2:8000/register-token/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'token': token}),
      );

      print("📤 Sent token to backend: ${response.body}");
    }
  } catch (e) {
    print("❌ Error fetching FCM token: $e");
  }
}

  /// ✅ Listen for foreground and background notifications
  void _setupFCMListeners() {
    /// Foreground Notifications
    FirebaseMessaging.onMessage
        .listen((RemoteMessage message) {
      print(
          "📩 Foreground Notification: ${message.notification?.title} - ${message.notification?.body}");

      // ✅ Show a native notification banner
      _showNotification(message.notification?.title,
          message.notification?.body);

      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Text(
              message.notification?.title ?? "No Title"),
          content:
              Text(message.notification?.body ?? "No Body"),
          actions: [
            TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text("OK"))
          ],
        ),
      );
    });

    /// Background Notifications (User taps notification)
    FirebaseMessaging.onMessageOpenedApp
        .listen((RemoteMessage message) {
      print(
          "🔄 Notification Clicked: ${message.notification?.title} - ${message.notification?.body}");
    });
  }

  /// ✅ Show a notification banner
  Future<void> _showNotification(
      String? title, String? body) async {
    const AndroidNotificationDetails
        androidPlatformChannelSpecifics =
        AndroidNotificationDetails(
      'high_importance_channel', // Channel ID
      'High Importance Notifications', // Channel name
      importance: Importance.high,
      priority: Priority.high,
    );

    const NotificationDetails platformChannelSpecifics =
        NotificationDetails(
            android: androidPlatformChannelSpecifics);

    await flutterLocalNotificationsPlugin.show(
      0, // Notification ID
      title ?? "No Title",
      body ?? "No Body",
      platformChannelSpecifics,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Demo app")),
      body: Center(
        child: Text("This is a demo app that receives notifications"),
      ),
    );
  }
}
