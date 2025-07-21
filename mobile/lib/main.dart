import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:http/http.dart' as http;
import 'package:mobile/config.dart';
import 'fullscreen_image_page.dart';

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

  const DarwinInitializationSettings iosInitializationSettings =
  DarwinInitializationSettings(
    requestAlertPermission: true,
    requestBadgePermission: true,
    requestSoundPermission: true,
  );

  const InitializationSettings initializationSettings =
      InitializationSettings(
    android: androidInitializationSettings,
    iOS: iosInitializationSettings,
  );

  await flutterLocalNotificationsPlugin
      .initialize(initializationSettings);

  await FirebaseMessaging.instance.requestPermission(
    alert: true,
    badge: true,
    sound: true,
  );

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
      final response = await http.post(
        Uri.parse('$apiBaseUrl/register-token/'),
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
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print("📩 Foreground Notification: ${message.notification?.title} - ${message.notification?.body}");
      print("📦 Data: ${message.data}");

      final title = message.notification?.title ?? "No Title";
      final body = message.notification?.body ?? "No Body";
      final timestamp = message.data['timestamp'];
      final imageUrl = message.data['image'];

      // Native notification
      _showNotification(title, body);

      // Show custom fall dialog
      showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: Text(title),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              if (timestamp != null)
                Text("🕒 $timestamp", style: TextStyle(fontSize: 14)),
              if (imageUrl != null && imageUrl.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 12.0),
                  child: Image.network(
                    imageUrl,
                    width: 250,
                    fit: BoxFit.contain,
                    errorBuilder: (context, error, stackTrace) =>
                        Text("⚠️ Failed to load image"),
                  ),
                ),
              Padding(
                padding: const EdgeInsets.only(top: 12.0),
                child: Text(body, textAlign: TextAlign.center),
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text("OK"),
            ),
            if (imageUrl != null && imageUrl.isNotEmpty)
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => FullscreenImagePage(imageUrl: imageUrl),
                    ),
                  );
                },
                child: Text("View Image"),
              ),
          ],
        ),
      );
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
