/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Dual-licensed under AGPL-3.0 and commercial license. See LICENSE for details.
 */

import { describeEast, Assert, TestImpl } from "@elaraai/east-node-std";
import { Carousel, Text } from "../../src/index.js";

describeEast("Carousel", (test) => {
    // =========================================================================
    // Basic Creation
    // =========================================================================

    test("creates carousel with single item", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ]));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").items.size(), 1n));
    });

    test("creates carousel with multiple items", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
            Text.Root("Slide 2"),
            Text.Root("Slide 3"),
        ]));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").items.size(), 3n));
    });

    test("creates carousel with no options - all options are none", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ]));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").index.hasTag("none"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").defaultIndex.hasTag("none"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerView.hasTag("none"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").loop.hasTag("none"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").autoplay.hasTag("none"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.hasTag("none"), true));
    });

    // =========================================================================
    // Index Options
    // =========================================================================

    test("creates carousel with index", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
            Text.Root("Slide 2"),
        ], {
            index: 1n,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").index.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").index.unwrap("some"), 1n));
    });

    test("creates carousel with defaultIndex", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1")    ,
            Text.Root("Slide 2"),
        ], {
            defaultIndex: 0n,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").defaultIndex.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").defaultIndex.unwrap("some"), 0n));
    });

    // =========================================================================
    // Slides Per View/Move
    // =========================================================================

    test("creates carousel with slidesPerView", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
            Text.Root("Slide 2"),
            Text.Root("Slide 3"),
        ], {
            slidesPerView: 2n,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerView.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerView.unwrap("some"), 2n));
    });

    test("creates carousel with slidesPerMove", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
            Text.Root("Slide 2"),
        ], {
            slidesPerMove: 1n,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerMove.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerMove.unwrap("some"), 1n));
    });

    // =========================================================================
    // Boolean Options
    // =========================================================================

    test("creates carousel with loop", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            loop: true,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").loop.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").loop.unwrap("some"), true));
    });

    test("creates carousel with autoplay", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            autoplay: true,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").autoplay.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").autoplay.unwrap("some"), true));
    });

    test("creates carousel with allowMouseDrag", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            allowMouseDrag: true,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").allowMouseDrag.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").allowMouseDrag.unwrap("some"), true));
    });

    test("creates carousel with showIndicators", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            showIndicators: true,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showIndicators.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showIndicators.unwrap("some"), true));
    });

    test("creates carousel with showControls", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            showControls: true,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showControls.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showControls.unwrap("some"), true));
    });

    // =========================================================================
    // Style Options
    // =========================================================================

    test("creates carousel with horizontal orientation", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            orientation: "horizontal",
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").orientation.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").orientation.unwrap("some").hasTag("horizontal"), true));
    });

    test("creates carousel with vertical orientation", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            orientation: "vertical",
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").orientation.unwrap("some").hasTag("vertical"), true));
    });

    test("creates carousel with spacing", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            spacing: "4",
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").spacing.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").spacing.unwrap("some"), "4"));
    });

    test("creates carousel with padding", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
        ], {
            padding: "2",
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").padding.hasTag("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").padding.unwrap("some"), "2"));
    });

    // =========================================================================
    // Combined Options
    // =========================================================================

    test("creates carousel with all options", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Slide 1"),
            Text.Root("Slide 2"),
            Text.Root("Slide 3"),
        ], {
            defaultIndex: 0n,
            slidesPerView: 2n,
            slidesPerMove: 1n,
            loop: true,
            autoplay: false,
            allowMouseDrag: true,
            showIndicators: true,
            showControls: true,
            orientation: "horizontal",
            spacing: "4",
            padding: "2",
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").items.size(), 3n));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").defaultIndex.unwrap("some"), 0n));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerView.unwrap("some"), 2n));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerMove.unwrap("some"), 1n));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").loop.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").autoplay.unwrap("some"), false));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").allowMouseDrag.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showIndicators.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showControls.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").orientation.unwrap("some").hasTag("horizontal"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").spacing.unwrap("some"), "4"));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").padding.unwrap("some"), "2"));
    });

    test("creates image carousel with indicators and controls", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Image 1"),
            Text.Root("Image 2"),
            Text.Root("Image 3"),
        ], {
            loop: true,
            showIndicators: true,
            showControls: true,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").loop.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showIndicators.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").showControls.unwrap("some"), true));
    });

    test("creates multi-slide carousel", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Product 1"),
            Text.Root("Product 2"),
            Text.Root("Product 3"),
            Text.Root("Product 4"),
        ], {
            slidesPerView: 3n,
            slidesPerMove: 1n,
            spacing: "4",
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerView.unwrap("some"), 3n));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerMove.unwrap("some"), 1n));
    });

    test("creates autoplay carousel", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Banner 1"),
            Text.Root("Banner 2"),
        ], {
            autoplay: true,
            loop: true,
            allowMouseDrag: true,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").autoplay.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").loop.unwrap("some"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").allowMouseDrag.unwrap("some"), true));
    });

    test("creates vertical carousel", $ => {
        const carousel = $.let(Carousel.Root([
            Text.Root("Testimonial 1"),
            Text.Root("Testimonial 2"),
        ], {
            orientation: "vertical",
            slidesPerView: 1n,
        }));

        $(Assert.equal(carousel.unwrap().unwrap("Carousel").style.unwrap("some").orientation.unwrap("some").hasTag("vertical"), true));
        $(Assert.equal(carousel.unwrap().unwrap("Carousel").slidesPerView.unwrap("some"), 1n));
    });
}, {   platformFns: TestImpl,});
