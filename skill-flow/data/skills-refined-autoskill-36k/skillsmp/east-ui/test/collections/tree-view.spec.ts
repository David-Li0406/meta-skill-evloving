/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { TreeView } from "../../src/collections/tree-view/index.js";
import { describeEast as describe, Assert, TestImpl } from "@elaraai/east-node-std";

describe("TreeView", (test) => {
    // =========================================================================
    // TreeView.Item - Basic
    // =========================================================================

    test("creates item without indicator", $ => {
        const item = $.let(TreeView.Item("file1", "index.ts"));

        $(Assert.equal(item.unwrap().unwrap("Item").value, "file1"));
        $(Assert.equal(item.unwrap().unwrap("Item").label, "index.ts"));
        $(Assert.equal(item.unwrap().unwrap("Item").indicator.hasTag("none"), true));
    });

    test("creates item with indicator", $ => {
        const item = $.let(TreeView.Item("readme", "README.md", { prefix: "far", name: "file" }));

        $(Assert.equal(item.unwrap().unwrap("Item").value, "readme"));
        $(Assert.equal(item.unwrap().unwrap("Item").indicator.hasTag("some"), true));
        $(Assert.equal(item.unwrap().unwrap("Item").indicator.unwrap("some").name, "file"));
        $(Assert.equal(item.unwrap().unwrap("Item").indicator.unwrap("some").prefix, "far"));
    });

    test("creates item with colored indicator", $ => {
        const item = $.let(TreeView.Item("index", "index.ts", { prefix: "fas", name: "file-code", color: "blue.500" }));

        $(Assert.equal(item.unwrap().unwrap("Item").indicator.unwrap("some").name, "file-code"));
        $(Assert.equal(item.unwrap().unwrap("Item").indicator.unwrap("some").style.unwrap("some").color.unwrap("some"), "blue.500"));
    });

    // =========================================================================
    // TreeView.Branch - Basic
    // =========================================================================

    test("creates branch with children", $ => {
        const branch = $.let(TreeView.Branch("src", "src", [
            TreeView.Item("file1", "index.ts"),
            TreeView.Item("file2", "utils.ts"),
        ]));

        $(Assert.equal(branch.unwrap().unwrap("Branch").value, "src"));
        $(Assert.equal(branch.unwrap().unwrap("Branch").label, "src"));
        $(Assert.equal(branch.unwrap().unwrap("Branch").indicator.hasTag("none"), true));
    });

    test("creates branch with indicator", $ => {
        const branch = $.let(TreeView.Branch("src", "src", [
            TreeView.Item("file1", "index.ts"),
        ], { prefix: "fas", name: "folder" }));

        $(Assert.equal(branch.unwrap().unwrap("Branch").indicator.hasTag("some"), true));
        $(Assert.equal(branch.unwrap().unwrap("Branch").indicator.unwrap("some").name, "folder"));
        $(Assert.equal(branch.unwrap().unwrap("Branch").indicator.unwrap("some").prefix, "fas"));
    });

    test("creates branch with colored indicator", $ => {
        const branch = $.let(TreeView.Branch("src", "src", [
            TreeView.Item("file1", "index.ts"),
        ], { prefix: "fas", name: "folder", color: "yellow.500" }));

        $(Assert.equal(branch.unwrap().unwrap("Branch").indicator.unwrap("some").style.unwrap("some").color.unwrap("some"), "yellow.500"));
    });

    test("creates disabled branch", $ => {
        const branch = $.let(TreeView.Branch("src", "src", [
            TreeView.Item("file1", "index.ts"),
        ], undefined, true));

        $(Assert.equal(branch.unwrap().unwrap("Branch").disabled.unwrap("some"), true));
    });

    // =========================================================================
    // TreeView.Branch - Nested
    // =========================================================================

    test("creates nested branches", $ => {
        const tree = $.let(TreeView.Branch("src", "src", [
            TreeView.Branch("components", "components", [
                TreeView.Item("button", "Button.tsx"),
            ]),
            TreeView.Item("index", "index.ts"),
        ]));

        $(Assert.equal(tree.unwrap().unwrap("Branch").value, "src"));
    });

    // =========================================================================
    // TreeView.Root - Basic
    // =========================================================================

    test("creates tree view with items", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
            TreeView.Item("file2", "utils.ts"),
        ]));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").label.hasTag("none"), true));
    });

    test("creates tree view with branches and items", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Branch("src", "src", [
                TreeView.Item("index", "index.ts"),
            ]),
            TreeView.Item("package", "package.json"),
        ]));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").label.hasTag("none"), true));
    });

    test("creates tree view with label", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
        ], {
            label: "Project Files",
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").label.unwrap("some"), "Project Files"));
    });

    // =========================================================================
    // TreeView.Root - Styling
    // =========================================================================

    test("creates tree view with subtle variant", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
        ], {
            variant: "subtle",
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
    });

    test("creates tree view with solid variant", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
        ], {
            variant: "solid",
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").style.unwrap("some").variant.unwrap("some").hasTag("solid"), true));
    });

    test("creates tree view with sm size", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
        ], {
            size: "sm",
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });

    test("creates tree view with single selection mode", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
        ], {
            selectionMode: "single",
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").style.unwrap("some").selectionMode.unwrap("some").hasTag("single"), true));
    });

    test("creates tree view with multiple selection mode", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
        ], {
            selectionMode: "multiple",
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").style.unwrap("some").selectionMode.unwrap("some").hasTag("multiple"), true));
    });

    // =========================================================================
    // TreeView.Root - Default Values
    // =========================================================================

    test("creates tree view with default expanded values", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Branch("src", "src", [
                TreeView.Item("file1", "index.ts"),
            ]),
        ], {
            defaultExpandedValue: ["src"],
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").defaultExpandedValue.hasTag("some"), true));
    });

    test("creates tree view with default selected values", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Item("file1", "index.ts"),
            TreeView.Item("file2", "utils.ts"),
        ], {
            defaultSelectedValue: ["file1"],
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").defaultSelectedValue.hasTag("some"), true));
    });

    // =========================================================================
    // TreeView - Complete File Explorer Example
    // =========================================================================

    test("creates complete file explorer with indicators", $ => {
        const tree = $.let(TreeView.Root([
            TreeView.Branch("src", "src", [
                TreeView.Branch("components", "components", [
                    TreeView.Item("button", "Button.tsx", { prefix: "fas", name: "file-code", color: "blue.500" }),
                    TreeView.Item("input", "Input.tsx", { prefix: "fas", name: "file-code", color: "blue.500" }),
                ], { prefix: "fas", name: "folder", color: "yellow.500" }),
                TreeView.Item("index", "index.ts", { prefix: "fas", name: "file-code", color: "blue.500" }),
            ], { prefix: "fas", name: "folder", color: "yellow.500" }),
            TreeView.Item("package", "package.json", { prefix: "far", name: "file" }),
            TreeView.Item("readme", "README.md", { prefix: "far", name: "file" }),
        ], {
            label: "Project",
            variant: "subtle",
            size: "sm",
            defaultExpandedValue: ["src", "components"],
        }));

        $(Assert.equal(tree.unwrap().unwrap("TreeView").label.unwrap("some"), "Project"));
        $(Assert.equal(tree.unwrap().unwrap("TreeView").style.unwrap("some").variant.unwrap("some").hasTag("subtle"), true));
        $(Assert.equal(tree.unwrap().unwrap("TreeView").style.unwrap("some").size.unwrap("some").hasTag("sm"), true));
    });
}, {   platformFns: TestImpl,});
