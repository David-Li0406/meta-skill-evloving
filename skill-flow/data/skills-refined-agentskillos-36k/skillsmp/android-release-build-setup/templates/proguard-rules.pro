# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in the Android SDK.

#===============================================================================
# DEBUGGING
#===============================================================================

# Keep line numbers for debugging stack traces
-keepattributes SourceFile,LineNumberTable

# Hide the original source file name
-renamesourcefileattribute SourceFile

#===============================================================================
# KOTLIN & ANDROID ESSENTIALS
#===============================================================================

# Keep Kotlin metadata
-keepattributes *Annotation*

# Keep data classes and their fields (Kotlin serialization)
-keepclassmembers class * {
    @kotlinx.serialization.SerialName <fields>;
}

# Keep Parcelables
-keepclassmembers class * implements android.os.Parcelable {
    public static final android.os.Parcelable$Creator *;
}

# Keep custom views
-keep public class * extends android.view.View {
    public <init>(android.content.Context);
    public <init>(android.content.Context, android.util.AttributeSet);
    public <init>(android.content.Context, android.util.AttributeSet, int);
}

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep enum classes
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}

#===============================================================================
# COMMON LIBRARY RULES
#===============================================================================
# Add rules for libraries your project uses below

# --- Gson ---
# Uncomment if using Gson
# -keepattributes Signature
# -keepattributes *Annotation*
# -dontwarn sun.misc.**
# -keep class * implements com.google.gson.TypeAdapter
# -keep class * implements com.google.gson.TypeAdapterFactory
# -keep class * implements com.google.gson.JsonSerializer
# -keep class * implements com.google.gson.JsonDeserializer
# -keepclassmembers,allowobfuscation class * {
#   @com.google.gson.annotations.SerializedName <fields>;
# }

# --- Retrofit 2 ---
# Uncomment if using Retrofit
# -dontwarn retrofit2.**
# -keep class retrofit2.** { *; }
# -keepattributes Signature
# -keepattributes Exceptions
# -keepclasseswithmembers class * {
#     @retrofit2.http.* <methods>;
# }

# --- OkHttp3 ---
# Uncomment if using OkHttp
# -dontwarn okhttp3.**
# -dontwarn okio.**
# -keep class okhttp3.** { *; }
# -keep interface okhttp3.** { *; }

# --- Room ---
# Uncomment if using Room
# -keep class * extends androidx.room.RoomDatabase
# -keep @androidx.room.Entity class *
# -dontwarn androidx.room.paging.**

# --- Glide ---
# Uncomment if using Glide
# -keep public class * implements com.bumptech.glide.module.GlideModule
# -keep class * extends com.bumptech.glide.module.AppGlideModule {
#  <init>(...);
# }
# -keep public enum com.bumptech.glide.load.ImageHeaderParser$** {
#   **[] $VALUES;
#   public *;
# }

#===============================================================================
# PROJECT-SPECIFIC RULES
#===============================================================================
# Add your project-specific keep rules below
