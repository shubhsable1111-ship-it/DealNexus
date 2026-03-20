// widgets/login_card.dart
import 'package:flutter/material.dart';

/// A reusable card widget for login options.
/// Displays the app name, a phone number input, an OTP button,
/// and a footer that changes based on the title.
class LoginCard extends StatefulWidget {
  /// The title displayed inside the card (e.g., "Customer Login", "Shop Owner Login")
  final String title;

  /// Optional custom footer text; if not provided, it will be generated from the title.
  final String? footerText;

  /// Callback invoked when the "Get OTP" button is pressed.
  /// Provides the entered phone number as a string.
  final void Function(String phoneNumber) onGetOtp;

  const LoginCard({
    super.key,
    required this.title,
    this.footerText,
    required this.onGetOtp,
  });

  @override
  State<LoginCard> createState() => _LoginCardState();
}

class _LoginCardState extends State<LoginCard> {
  final TextEditingController _phoneController = TextEditingController();

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }

  String _getFooterText() {
    if (widget.footerText != null) return widget.footerText!;
    // Determine footer text based on title
    if (widget.title.toLowerCase().contains('customer')) {
      return 'Sign Up';
    } else if (widget.title.toLowerCase().contains('shop')) {
      return 'Register Now';
    }
    return 'Create Account'; // fallback
  }

  void _handleGetOtp() {
    final phone = _phoneController.text.trim();
    widget.onGetOtp(phone);
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // App name
            const Text(
              'OfferZone',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Color(0xFFFF6F00),
              ),
            ),
            const SizedBox(height: 16),
            // Title
            Text(
              widget.title,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600,
                color: Colors.black87,
              ),
            ),
            const SizedBox(height: 24),
            // Phone number input
            TextFormField(
              controller: _phoneController,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(
                labelText: 'Phone Number',
                prefix: const Text('+91 '),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: const BorderSide(color: Color(0xFFFF6F00), width: 2),
                ),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 14,
                ),
              ),
            ),
            const SizedBox(height: 24),
            // Orange OTP button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _handleGetOtp,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFFFF6F00),
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  textStyle: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                child: const Text('GET OTP'),
              ),
            ),
            const SizedBox(height: 16),
            // Footer text
            Align(
              alignment: Alignment.center,
              child: TextButton(
                onPressed: () {
                  // Footer action can be handled by the parent if needed.
                  // For now, we leave it as a placeholder.
                },
                style: TextButton.styleFrom(
                  foregroundColor: const Color(0xFFFF6F00),
                ),
                child: Text(_getFooterText()),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
