package com.example.demo.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.annotation.Nullable;

import java.time.Instant;
import java.util.List;

/**
 * 使用者偏好設定
 * 對應 JSON 中的 preferences 巢狀物件
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public record UserPreferences(
        String theme,
        String language,
        List<String> notifications) {
}

/**
 * 使用者資料
 * 從 API 回應的 JSON 轉換而來
 */
@JsonIgnoreProperties(ignoreUnknown = true)
public record UserRecord(
        @JsonProperty("user_id") Long userId,

        String username,

        String email,

        @JsonProperty("is_active") Boolean isActive,

        UserPreferences preferences,

        List<String> roles,

        @JsonProperty("last_login") Instant lastLogin,

        @Nullable @JsonProperty("meta_tags") List<String> metaTags) {
}
