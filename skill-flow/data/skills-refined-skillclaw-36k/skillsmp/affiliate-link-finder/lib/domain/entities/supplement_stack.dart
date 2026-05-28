class SupplementStack {
  final String id;
  final String userId;
  final String name;
  final List<StackItem> items;
  final String? timeOfDay;
  final DateTime createdAt;
  final DateTime updatedAt;

  const SupplementStack({
    required this.id,
    required this.userId,
    required this.name,
    required this.items,
    this.timeOfDay,
    required this.createdAt,
    required this.updatedAt,
  });

  SupplementStack copyWith({
    String? id,
    String? userId,
    String? name,
    List<StackItem>? items,
    String? timeOfDay,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return SupplementStack(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      name: name ?? this.name,
      items: items ?? this.items,
      timeOfDay: timeOfDay ?? this.timeOfDay,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'name': name,
      'items': items.map((item) => item.toJson()).toList(),
      'timeOfDay': timeOfDay,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
    };
  }

  factory SupplementStack.fromJson(Map<String, dynamic> json) {
    return SupplementStack(
      id: json['id'] as String,
      userId: json['userId'] as String,
      name: json['name'] as String,
      items: (json['items'] as List<dynamic>)
          .map((item) => StackItem.fromJson(item as Map<String, dynamic>))
          .toList(),
      timeOfDay: json['timeOfDay'] as String?,
      createdAt: DateTime.parse(json['createdAt'] as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
    );
  }
}

class StackItem {
  final String supplementId;
  final String? customDosage;
  final String? customNotes;
  final String? scheduledTime;
  final int order;

  const StackItem({
    required this.supplementId,
    this.customDosage,
    this.customNotes,
    this.scheduledTime,
    required this.order,
  });

  StackItem copyWith({
    String? supplementId,
    String? customDosage,
    String? customNotes,
    String? scheduledTime,
    int? order,
  }) {
    return StackItem(
      supplementId: supplementId ?? this.supplementId,
      customDosage: customDosage ?? this.customDosage,
      customNotes: customNotes ?? this.customNotes,
      scheduledTime: scheduledTime ?? this.scheduledTime,
      order: order ?? this.order,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'supplementId': supplementId,
      'customDosage': customDosage,
      'customNotes': customNotes,
      'scheduledTime': scheduledTime,
      'order': order,
    };
  }

  factory StackItem.fromJson(Map<String, dynamic> json) {
    return StackItem(
      supplementId: json['supplementId'] as String,
      customDosage: json['customDosage'] as String?,
      customNotes: json['customNotes'] as String?,
      scheduledTime: json['scheduledTime'] as String?,
      order: json['order'] as int,
    );
  }
}
