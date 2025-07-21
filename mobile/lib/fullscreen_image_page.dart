import 'package:flutter/material.dart';

class FullscreenImagePage extends StatelessWidget {
  final String imageUrl;

  const FullscreenImagePage({Key? key, required this.imageUrl}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Fall Image")),
      backgroundColor: Colors.black,
      body: Center(
        child: InteractiveViewer(
          child: Image.network(
            imageUrl,
            fit: BoxFit.contain,
            errorBuilder: (context, error, stackTrace) =>
                Text("⚠️ Failed to load image", style: TextStyle(color: Colors.white)),
          ),
        ),
      ),
    );
  }
}