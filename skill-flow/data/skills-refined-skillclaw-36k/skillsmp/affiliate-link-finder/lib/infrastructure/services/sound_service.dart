import 'package:audioplayers/audioplayers.dart';
import '../../utils/logger.dart';

class SoundService {
  final AudioPlayer _player = AudioPlayer();

  SoundService() {
    // Pre-load or configure if needed
  }

  Future<void> playSuccess() async {
    try {
      // Using Source from assets directory
      await _player.play(AssetSource('sounds/success.mp3'));
    } catch (e) {
      AppLogger.e('Failed to play success sound', e);
    }
  }

  Future<void> dispose() async {
    await _player.dispose();
  }
}
