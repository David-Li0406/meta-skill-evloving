import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../application/providers/auth_provider.dart';
import '../views/auth/login_screen.dart';
import '../views/medical_disclaimer_screen.dart';
import '../views/dashboard_screen.dart';

class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<AuthProvider>(
      builder: (context, auth, _) {
        switch (auth.status) {
          case AuthStatus.initial:
            return const Scaffold(
              body: Center(
                child: CircularProgressIndicator(),
              ),
            );
          case AuthStatus.authenticated:
            if (auth.user?.hasCompletedOnboarding == false) {
              return const MedicalDisclaimerScreen();
            }
            return const DashboardScreen();
          case AuthStatus.unauthenticated:
            return const LoginScreen();
        }
      },
    );
  }
}
