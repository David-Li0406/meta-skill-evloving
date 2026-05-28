import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'skeleton_loader.dart';

class CachedImage extends StatelessWidget {
  /// The URL of the image to display.
  final String imageUrl;

  /// Optional width for the image.
  final double? width;

  /// Optional height for the image.
  final double? height;

  /// How the image should be inscribed into the box.
  /// Defaults to [BoxFit.cover].
  final BoxFit? fit;

  /// The border radius for the image.
  /// Defaults to 0.
  final double borderRadius;

  /// Optional custom placeholder to show while loading.
  /// If null, [SkeletonLoader] is used.
  final Widget? placeholder;

  /// Optional custom widget to show on error.
  final Widget? errorWidget;

  /// A wrapper around [CachedNetworkImage] with ADHD-friendly loading states.
  ///
  /// This widget provides:
  /// - Automatic [SkeletonLoader] shimmer while loading.
  /// - Optional [borderRadius] with [ClipRRect].
  /// - Consistent error state handling.
  /// - 300ms fade-in transition for reduced visual jar.
  const CachedImage({
    super.key,
    required this.imageUrl,
    this.width,
    this.height,
    this.fit = BoxFit.cover,
    this.borderRadius = 0,
    this.placeholder,
    this.errorWidget,
  });

  @override
  Widget build(BuildContext context) {
    if (imageUrl.isEmpty) {
      return _buildError(context);
    }

    return ClipRRect(
      borderRadius: BorderRadius.circular(borderRadius),
      child: CachedNetworkImage(
        imageUrl: imageUrl,
        width: width,
        height: height,
        fit: fit, // Use the passed fit or default
        fadeInDuration: const Duration(milliseconds: 300),
        placeholder: (context, url) =>
            placeholder ?? _buildPlaceholder(context),
        errorWidget: (context, url, error) =>
            errorWidget ?? _buildError(context),
      ),
    );
  }

  Widget _buildPlaceholder(BuildContext context) {
    return SkeletonLoader(
      width: width ?? double.infinity,
      height: height ?? 200, // Reasonable default for placeholders
      borderRadius: borderRadius,
    );
  }

  Widget _buildError(BuildContext context) {
    return Container(
      width: width,
      height: height,
      color: Colors.red[50],
      child: Icon(
        Icons.broken_image_rounded,
        color: Colors.red[200],
        size: 24,
      ),
    );
  }
}
