/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import {
    type SubtypeExprOrValue,
    OptionType,
    StructType,
    StringType,
    IntegerType,
    BooleanType,
    VariantType,
    NullType,
    ArrayType,
    FunctionType,
} from "@elaraai/east";

// ============================================================================
// File Capture Type
// ============================================================================

/**
 * Capture mode for camera access on mobile devices.
 *
 * @remarks
 * Controls which camera to use when capturing media files.
 *
 * @property user - Front-facing camera (selfie mode)
 * @property environment - Rear-facing camera
 */
export const FileCaptureType = VariantType({
    /** Front-facing camera (selfie mode) */
    user: NullType,
    /** Rear-facing camera */
    environment: NullType,
});

/**
 * Type representing the FileCapture structure.
 */
export type FileCaptureType = typeof FileCaptureType;

/**
 * String literal type for capture values.
 */
export type FileCaptureLiteral = "user" | "environment";

// ============================================================================
// File Info Types for Callbacks
// ============================================================================

/**
 * Type for file information in callbacks.
 *
 * @property name - File name
 * @property size - File size in bytes
 * @property type - MIME type of the file
 */
export const FileInfoType = StructType({
    name: StringType,
    size: IntegerType,
    type: StringType,
});

export type FileInfoType = typeof FileInfoType;

/**
 * Type for file rejection information in callbacks.
 *
 * @property file - The rejected file info
 * @property errors - Array of error messages
 */
export const FileRejectionType = StructType({
    file: FileInfoType,
    errors: ArrayType(StringType),
});

export type FileRejectionType = typeof FileRejectionType;

// ============================================================================
// File Upload Type
// ============================================================================

/**
 * Type for FileUpload component data.
 *
 * @remarks
 * FileUpload is a form control for uploading files with drag-and-drop support.
 *
 * @property accept - Accepted file types (MIME type pattern, e.g., "image/*" or ".pdf,.doc")
 * @property maxFiles - Maximum number of files allowed
 * @property maxFileSize - Maximum file size in bytes
 * @property minFileSize - Minimum file size in bytes
 * @property directory - Whether to allow folder/directory upload
 * @property disabled - Whether the upload is disabled
 * @property required - Whether file upload is required
 * @property allowDrop - Whether to allow drag-and-drop
 * @property capture - Camera capture mode for mobile devices
 * @property name - Form input name attribute
 * @property label - Label text for the upload area
 * @property dropzoneText - Text shown in the dropzone area
 * @property triggerText - Text for the upload trigger button
 * @property onFileAccept - Callback triggered when files are accepted
 * @property onFileReject - Callback triggered when files are rejected
 */
export const FileUploadType = StructType({
    /** Accepted file types (MIME type pattern, e.g., "image/*" or ".pdf,.doc") */
    accept: OptionType(StringType),
    /** Maximum number of files allowed */
    maxFiles: OptionType(IntegerType),
    /** Maximum file size in bytes */
    maxFileSize: OptionType(IntegerType),
    /** Minimum file size in bytes */
    minFileSize: OptionType(IntegerType),
    /** Whether to allow folder/directory upload */
    directory: OptionType(BooleanType),
    /** Whether the upload is disabled */
    disabled: OptionType(BooleanType),
    /** Whether file upload is required */
    required: OptionType(BooleanType),
    /** Whether to allow drag-and-drop */
    allowDrop: OptionType(BooleanType),
    /** Camera capture mode for mobile devices */
    capture: OptionType(FileCaptureType),
    /** Form input name attribute */
    name: OptionType(StringType),
    /** Label text for the upload area */
    label: OptionType(StringType),
    /** Text shown in the dropzone area */
    dropzoneText: OptionType(StringType),
    /** Text for the upload trigger button */
    triggerText: OptionType(StringType),
    /** Callback triggered when files are accepted */
    onFileAccept: OptionType(FunctionType([ArrayType(FileInfoType)], NullType)),
    /** Callback triggered when files are rejected */
    onFileReject: OptionType(FunctionType([ArrayType(FileRejectionType)], NullType)),
});

/**
 * Type representing the FileUpload structure.
 */
export type FileUploadType = typeof FileUploadType;

// ============================================================================
// File Upload Style Interface
// ============================================================================

/**
 * TypeScript interface for FileUpload configuration options.
 *
 * @property accept - Accepted file types (MIME type pattern, e.g., "image/*" or ".pdf,.doc")
 * @property maxFiles - Maximum number of files allowed
 * @property maxFileSize - Maximum file size in bytes
 * @property minFileSize - Minimum file size in bytes
 * @property directory - Whether to allow folder/directory upload
 * @property disabled - Whether the upload is disabled
 * @property required - Whether file upload is required
 * @property allowDrop - Whether to allow drag-and-drop
 * @property capture - Camera capture mode for mobile devices
 * @property name - Form input name attribute
 * @property label - Label text for the upload area
 * @property dropzoneText - Text shown in the dropzone area
 * @property triggerText - Text for the upload trigger button
 * @property onFileAccept - Callback triggered when files are accepted
 * @property onFileReject - Callback triggered when files are rejected
 */
export interface FileUploadStyle {
    /** Accepted file types (MIME type pattern, e.g., "image/*" or ".pdf,.doc") */
    accept?: SubtypeExprOrValue<StringType>;
    /** Maximum number of files allowed */
    maxFiles?: SubtypeExprOrValue<IntegerType> | number;
    /** Maximum file size in bytes */
    maxFileSize?: SubtypeExprOrValue<IntegerType> | number;
    /** Minimum file size in bytes */
    minFileSize?: SubtypeExprOrValue<IntegerType> | number;
    /** Whether to allow folder/directory upload */
    directory?: SubtypeExprOrValue<BooleanType>;
    /** Whether the upload is disabled */
    disabled?: SubtypeExprOrValue<BooleanType>;
    /** Whether file upload is required */
    required?: SubtypeExprOrValue<BooleanType>;
    /** Whether to allow drag-and-drop */
    allowDrop?: SubtypeExprOrValue<BooleanType>;
    /** Camera capture mode for mobile devices */
    capture?: SubtypeExprOrValue<FileCaptureType> | FileCaptureLiteral;
    /** Form input name attribute */
    name?: SubtypeExprOrValue<StringType>;
    /** Label text for the upload area */
    label?: SubtypeExprOrValue<StringType>;
    /** Text shown in the dropzone area */
    dropzoneText?: SubtypeExprOrValue<StringType>;
    /** Text for the upload trigger button */
    triggerText?: SubtypeExprOrValue<StringType>;
    /** Callback triggered when files are accepted */
    onFileAccept?: SubtypeExprOrValue<FunctionType<[ArrayType<FileInfoType>], NullType>>;
    /** Callback triggered when files are rejected */
    onFileReject?: SubtypeExprOrValue<FunctionType<[ArrayType<FileRejectionType>], NullType>>;
}
