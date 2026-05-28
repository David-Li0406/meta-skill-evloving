/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { FileUpload } from "../../src/index.js";

describeEast("FileUpload", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates file upload with no options", $ => {
        const upload = $.let(FileUpload.Root());

        $(Assert.equal(upload.unwrap().getTag(), "FileUpload"));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.hasTag("none"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFiles.hasTag("none"), true));
    });

    test("creates file upload with label", $ => {
        const upload = $.let(FileUpload.Root({
            label: "Upload file",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").label.hasTag("some"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").label.unwrap("some"), "Upload file"));
    });

    test("creates file upload with trigger text", $ => {
        const upload = $.let(FileUpload.Root({
            triggerText: "Choose file",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").triggerText.unwrap("some"), "Choose file"));
    });

    test("creates file upload with dropzone text", $ => {
        const upload = $.let(FileUpload.Root({
            dropzoneText: "or drag and drop here",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").dropzoneText.unwrap("some"), "or drag and drop here"));
    });

    // =========================================================================
    // Accept Patterns
    // =========================================================================

    test("creates file upload with image accept pattern", $ => {
        const upload = $.let(FileUpload.Root({
            accept: "image/*",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.hasTag("some"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.unwrap("some"), "image/*"));
    });

    test("creates file upload with specific extensions", $ => {
        const upload = $.let(FileUpload.Root({
            accept: ".pdf,.doc,.docx",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.unwrap("some"), ".pdf,.doc,.docx"));
    });

    test("creates file upload with video accept pattern", $ => {
        const upload = $.let(FileUpload.Root({
            accept: "video/*",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.unwrap("some"), "video/*"));
    });

    // =========================================================================
    // File Constraints
    // =========================================================================

    test("creates file upload with maxFiles", $ => {
        const upload = $.let(FileUpload.Root({
            maxFiles: 5,
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFiles.hasTag("some"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFiles.unwrap("some"), 5n));
    });

    test("creates file upload with maxFileSize", $ => {
        const upload = $.let(FileUpload.Root({
            maxFileSize: 5 * 1024 * 1024, // 5MB
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFileSize.hasTag("some"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFileSize.unwrap("some"), 5242880n));
    });

    test("creates file upload with minFileSize", $ => {
        const upload = $.let(FileUpload.Root({
            minFileSize: 1024, // 1KB
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").minFileSize.unwrap("some"), 1024n));
    });

    test("creates file upload with all size constraints", $ => {
        const upload = $.let(FileUpload.Root({
            maxFiles: 3,
            maxFileSize: 10 * 1024 * 1024,
            minFileSize: 100,
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFiles.unwrap("some"), 3n));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFileSize.unwrap("some"), 10485760n));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").minFileSize.unwrap("some"), 100n));
    });

    // =========================================================================
    // Behavior Options
    // =========================================================================

    test("creates file upload with directory enabled", $ => {
        const upload = $.let(FileUpload.Root({
            directory: true,
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").directory.hasTag("some"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").directory.unwrap("some"), true));
    });

    test("creates file upload disabled", $ => {
        const upload = $.let(FileUpload.Root({
            disabled: true,
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").disabled.unwrap("some"), true));
    });

    test("creates required file upload", $ => {
        const upload = $.let(FileUpload.Root({
            required: true,
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").required.unwrap("some"), true));
    });

    test("creates file upload with allowDrop disabled", $ => {
        const upload = $.let(FileUpload.Root({
            allowDrop: false,
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").allowDrop.unwrap("some"), false));
    });

    test("creates file upload with name", $ => {
        const upload = $.let(FileUpload.Root({
            name: "document",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").name.unwrap("some"), "document"));
    });

    // =========================================================================
    // Capture Mode
    // =========================================================================

    test("creates file upload with user camera capture", $ => {
        const upload = $.let(FileUpload.Root({
            capture: "user",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").capture.hasTag("some"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").capture.unwrap("some").hasTag("user"), true));
    });

    test("creates file upload with environment camera capture", $ => {
        const upload = $.let(FileUpload.Root({
            capture: "environment",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").capture.unwrap("some").hasTag("environment"), true));
    });

    // =========================================================================
    // Practical Examples
    // =========================================================================

    test("creates image upload with drag-and-drop", $ => {
        const upload = $.let(FileUpload.Root({
            accept: "image/*",
            maxFiles: 5,
            maxFileSize: 5 * 1024 * 1024,
            label: "Upload images",
            dropzoneText: "or drag and drop here",
            triggerText: "Choose files",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.unwrap("some"), "image/*"));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFiles.unwrap("some"), 5n));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").label.unwrap("some"), "Upload images"));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").dropzoneText.unwrap("some"), "or drag and drop here"));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").triggerText.unwrap("some"), "Choose files"));
    });

    test("creates single document upload", $ => {
        const upload = $.let(FileUpload.Root({
            accept: ".pdf",
            maxFiles: 1,
            required: true,
            label: "Upload document",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.unwrap("some"), ".pdf"));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFiles.unwrap("some"), 1n));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").required.unwrap("some"), true));
    });

    test("creates folder upload", $ => {
        const upload = $.let(FileUpload.Root({
            directory: true,
            label: "Upload folder",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").directory.unwrap("some"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").label.unwrap("some"), "Upload folder"));
    });

    test("creates mobile camera capture upload", $ => {
        const upload = $.let(FileUpload.Root({
            accept: "image/*",
            capture: "environment",
            maxFiles: 1,
            label: "Take photo",
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").accept.unwrap("some"), "image/*"));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").capture.unwrap("some").hasTag("environment"), true));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").label.unwrap("some"), "Take photo"));
    });

    test("creates bulk file upload", $ => {
        const upload = $.let(FileUpload.Root({
            maxFiles: 100,
            maxFileSize: 50 * 1024 * 1024, // 50MB
            label: "Upload files",
            dropzoneText: "Drop files here or click to browse",
            triggerText: "Select files",
            allowDrop: true,
        }));

        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFiles.unwrap("some"), 100n));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").maxFileSize.unwrap("some"), 52428800n));
        $(Assert.equal(upload.unwrap().unwrap("FileUpload").allowDrop.unwrap("some"), true));
    });
}, {   platformFns: TestImpl,});
