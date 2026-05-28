import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'package:adhd_supplement_app/application/view_models/supplement_view_model.dart';
import 'package:adhd_supplement_app/presentation/views/supplement_detail.dart';

class HomeView extends StatelessWidget {
  const HomeView({super.key});

  @override
  Widget build(BuildContext context) {
    // final viewModel = context.watch<SupplementViewModel>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('ADHD Education'),
        centerTitle: true,
      ),
      body: Consumer<SupplementViewModel>(
        builder: (context, viewModel, child) {
          if (viewModel.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          if (viewModel.error != null) {
            return Center(child: Text(viewModel.error!));
          }

          return ListView.builder(
            itemCount: viewModel.supplements.length,
            itemBuilder: (context, index) {
              final supplement = viewModel.supplements[index];
              return Card(
                margin: const EdgeInsets.all(8.0),
                child: ListTile(
                  title: Text(supplement.name),
                  subtitle: Text(supplement.description),
                  trailing: const Icon(Icons.arrow_forward_ios),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute<void>(
                        builder: (context) =>
                            SupplementDetail(supplement: supplement),
                      ),
                    );
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}
