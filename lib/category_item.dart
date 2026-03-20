// widgets/category_item.dart
import 'package:flutter/material.dart';

/// A circular category item with an icon and a title label.
/// Typically used in a horizontal list to represent different product categories.
class CategoryItem extends StatelessWidget {
  /// The text label shown below the icon.
  final String title;

  /// The icon displayed inside the circular background.
  final IconData icon;

  /// Optional custom background color for the circle.
  /// Defaults to a soft grey (Colors.grey.shade200).
  final Color? backgroundColor;

  /// Optional custom icon color. Defaults to the app's primary orange.
  final Color? iconColor;

  /// Optional size of the circular container. Defaults to 70.
  final double size;

  const CategoryItem({
    super.key,
    required this.title,
    required this.icon,
    this.backgroundColor,
    this.iconColor,
    this.size = 70,
  });

  @override
  Widget build(BuildContext context) {
    // Use default soft background if not provided
    final bgColor = backgroundColor ?? Colors.grey.shade200;
    // Use default orange if not provided
    final color = iconColor ?? const Color(0xFFFF6F00);

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            color: bgColor,
            shape: BoxShape.circle,
          ),
          child: Icon(
            icon,
            size: size * 0.45, // icon size proportional to container
            color: color,
          ),
        ),
        const SizedBox(height: 8),
        Text(
          title,
          style: const TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w500,
            color: Colors.black87,
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}