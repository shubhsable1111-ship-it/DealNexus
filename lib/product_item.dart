// widgets/product_item.dart
import 'package:flutter/material.dart';

/// A product item widget for cart screens.
/// Displays product image, name, price, and quantity controls.
class ProductItem extends StatefulWidget {
  /// Product name
  final String name;

  /// Product price (per unit)
  final double price;

  /// Initial quantity (defaults to 1)
  final int initialQuantity;

  /// URL of the product image
  final String imageUrl;

  /// Callback when quantity changes (returns the new quantity)
  final void Function(int newQuantity)? onQuantityChanged;

  const ProductItem({
    super.key,
    required this.name,
    required this.price,
    this.initialQuantity = 1,
    required this.imageUrl,
    this.onQuantityChanged,
  });

  @override
  State<ProductItem> createState() => _ProductItemState();
}

class _ProductItemState extends State<ProductItem> {
  late int _quantity;

  @override
  void initState() {
    super.initState();
    _quantity = widget.initialQuantity;
  }

  void _increment() {
    setState(() {
      _quantity++;
    });
    widget.onQuantityChanged?.call(_quantity);
  }

  void _decrement() {
    if (_quantity > 1) {
      setState(() {
        _quantity--;
      });
      widget.onQuantityChanged?.call(_quantity);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 0),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
      ),
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Product image
            ClipRRect(
              borderRadius: BorderRadius.circular(8),
              child: Image.network(
                widget.imageUrl,
                width: 70,
                height: 70,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) {
                  return Container(
                    width: 70,
                    height: 70,
                    color: Colors.grey[200],
                    child: const Icon(Icons.image_not_supported),
                  );
                },
              ),
            ),
            const SizedBox(width: 12),
            // Name and price
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    widget.name,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '₹${widget.price.toStringAsFixed(0)}',
                    style: const TextStyle(
                      fontSize: 14,
                      color: Colors.grey,
                    ),
                  ),
                ],
              ),
            ),
            // Quantity controls
            Row(
              children: [
                IconButton(
                  onPressed: _decrement,
                  icon: const Icon(Icons.remove),
                  constraints: const BoxConstraints(minWidth: 32, minHeight: 32),
                  style: IconButton.styleFrom(
                    backgroundColor: Colors.grey[200],
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    padding: EdgeInsets.zero,
                  ),
                ),
                const SizedBox(width: 8),
                SizedBox(
                  width: 40,
                  child: Text(
                    '$_quantity',
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: _increment,
                  icon: const Icon(Icons.add),
                  constraints: const BoxConstraints(minWidth: 32, minHeight: 32),
                  style: IconButton.styleFrom(
                    backgroundColor: const Color(0xFFFF6F00).withOpacity(0.1),
                    foregroundColor: const Color(0xFFFF6F00),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                    padding: EdgeInsets.zero,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}