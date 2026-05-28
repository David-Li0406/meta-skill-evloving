// MARK: - AppKit MKMapView Integration
// macOS AppKit MKMapView統合例

import SwiftUI
import MapKit
import AppKit

// MARK: - NSViewRepresentable ラッパー

/// AppKit MKMapViewをSwiftUIで使用するためのラッパー
struct AppKitMapView: NSViewRepresentable {
    @Binding var region: MKCoordinateRegion
    var annotations: [MKAnnotation]
    var showsUserLocation: Bool = true
    var mapType: MKMapType = .standard

    // MARK: - NSViewRepresentable

    func makeNSView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator

        // 基本設定
        mapView.showsUserLocation = showsUserLocation
        mapView.showsCompass = true
        mapView.showsZoomControls = true
        mapView.showsScale = true

        // 操作設定
        mapView.isZoomEnabled = true
        mapView.isScrollEnabled = true
        mapView.isRotateEnabled = true
        mapView.isPitchEnabled = true

        return mapView
    }

    func updateNSView(_ mapView: MKMapView, context: Context) {
        // 地域更新
        if !context.coordinator.isUserInteracting {
            mapView.setRegion(region, animated: true)
        }

        // 地図タイプ更新
        mapView.mapType = mapType

        // アノテーション更新
        updateAnnotations(mapView: mapView)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    // MARK: - Private Methods

    private func updateAnnotations(mapView: MKMapView) {
        // 既存のアノテーションを削除（ユーザー位置以外）
        let existingAnnotations = mapView.annotations.filter { !($0 is MKUserLocation) }
        mapView.removeAnnotations(existingAnnotations)

        // 新しいアノテーションを追加
        mapView.addAnnotations(annotations)
    }

    // MARK: - Coordinator

    class Coordinator: NSObject, MKMapViewDelegate {
        var parent: AppKitMapView
        var isUserInteracting = false

        init(_ parent: AppKitMapView) {
            self.parent = parent
        }

        // MARK: - MKMapViewDelegate

        func mapView(_ mapView: MKMapView, regionWillChangeAnimated animated: Bool) {
            isUserInteracting = true
        }

        func mapView(_ mapView: MKMapView, regionDidChangeAnimated animated: Bool) {
            isUserInteracting = false
            DispatchQueue.main.async {
                self.parent.region = mapView.region
            }
        }

        func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
            // ユーザー位置はデフォルト表示
            guard !(annotation is MKUserLocation) else { return nil }

            let identifier = "CustomAnnotation"
            var annotationView = mapView.dequeueReusableAnnotationView(withIdentifier: identifier) as? MKMarkerAnnotationView

            if annotationView == nil {
                annotationView = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: identifier)
                annotationView?.canShowCallout = true
                annotationView?.rightCalloutAccessoryView = NSButton(title: "詳細", target: nil, action: nil)
            } else {
                annotationView?.annotation = annotation
            }

            return annotationView
        }

        func mapView(_ mapView: MKMapView, annotationView view: MKAnnotationView, calloutAccessoryControlTapped control: NSView) {
            guard let annotation = view.annotation else { return }
            print("Callout tapped for: \(annotation.title ?? "Unknown")")
        }

        func mapView(_ mapView: MKMapView, didSelect annotation: MKAnnotation) {
            print("Selected: \(annotation.title ?? "Unknown")")
        }

        func mapView(_ mapView: MKMapView, didDeselect annotation: MKAnnotation) {
            print("Deselected: \(annotation.title ?? "Unknown")")
        }

        func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
            if let polyline = overlay as? MKPolyline {
                let renderer = MKPolylineRenderer(polyline: polyline)
                renderer.strokeColor = .systemBlue
                renderer.lineWidth = 4
                return renderer
            }

            if let circle = overlay as? MKCircle {
                let renderer = MKCircleRenderer(circle: circle)
                renderer.fillColor = NSColor.systemBlue.withAlphaComponent(0.2)
                renderer.strokeColor = .systemBlue
                renderer.lineWidth = 2
                return renderer
            }

            return MKOverlayRenderer(overlay: overlay)
        }
    }
}

// MARK: - カスタムアノテーション

/// カスタムアノテーションクラス
final class CustomAnnotation: NSObject, MKAnnotation {
    let coordinate: CLLocationCoordinate2D
    let title: String?
    let subtitle: String?
    let identifier: String

    init(coordinate: CLLocationCoordinate2D, title: String?, subtitle: String? = nil, identifier: String = UUID().uuidString) {
        self.coordinate = coordinate
        self.title = title
        self.subtitle = subtitle
        self.identifier = identifier
        super.init()
    }
}

// MARK: - オーバーレイ付きMapView

/// オーバーレイをサポートするMapView
struct AppKitMapViewWithOverlays: NSViewRepresentable {
    @Binding var region: MKCoordinateRegion
    var annotations: [MKAnnotation]
    var overlays: [MKOverlay]

    func makeNSView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        mapView.showsUserLocation = true
        mapView.showsZoomControls = true
        return mapView
    }

    func updateNSView(_ mapView: MKMapView, context: Context) {
        mapView.setRegion(region, animated: true)

        // アノテーション更新
        let existingAnnotations = mapView.annotations.filter { !($0 is MKUserLocation) }
        mapView.removeAnnotations(existingAnnotations)
        mapView.addAnnotations(annotations)

        // オーバーレイ更新
        mapView.removeOverlays(mapView.overlays)
        mapView.addOverlays(overlays)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    class Coordinator: NSObject, MKMapViewDelegate {
        func mapView(_ mapView: MKMapView, viewFor annotation: MKAnnotation) -> MKAnnotationView? {
            guard !(annotation is MKUserLocation) else { return nil }

            let view = MKMarkerAnnotationView(annotation: annotation, reuseIdentifier: nil)
            view.canShowCallout = true
            return view
        }

        func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
            if let polyline = overlay as? MKPolyline {
                let renderer = MKPolylineRenderer(polyline: polyline)
                renderer.strokeColor = .systemBlue
                renderer.lineWidth = 4
                return renderer
            }

            if let circle = overlay as? MKCircle {
                let renderer = MKCircleRenderer(circle: circle)
                renderer.fillColor = NSColor.systemBlue.withAlphaComponent(0.2)
                renderer.strokeColor = .systemBlue
                renderer.lineWidth = 2
                return renderer
            }

            if let polygon = overlay as? MKPolygon {
                let renderer = MKPolygonRenderer(polygon: polygon)
                renderer.fillColor = NSColor.systemGreen.withAlphaComponent(0.2)
                renderer.strokeColor = .systemGreen
                renderer.lineWidth = 2
                return renderer
            }

            return MKOverlayRenderer(overlay: overlay)
        }
    }
}

// MARK: - 使用例View

/// AppKit MapViewの使用例
struct AppKitMapExampleView: View {
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    )

    @State private var annotations: [MKAnnotation] = [
        CustomAnnotation(
            coordinate: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
            title: "東京駅",
            subtitle: "JR東日本"
        ),
        CustomAnnotation(
            coordinate: CLLocationCoordinate2D(latitude: 35.6580, longitude: 139.7016),
            title: "渋谷駅",
            subtitle: "JR東日本・東急"
        )
    ]

    @State private var selectedMapType: MKMapType = .standard

    var body: some View {
        VStack {
            AppKitMapView(
                region: $region,
                annotations: annotations,
                mapType: selectedMapType
            )

            HStack {
                Picker("地図タイプ", selection: $selectedMapType) {
                    Text("標準").tag(MKMapType.standard)
                    Text("衛星").tag(MKMapType.satellite)
                    Text("ハイブリッド").tag(MKMapType.hybrid)
                }
                .pickerStyle(.segmented)
                .frame(maxWidth: 300)

                Spacer()

                Button("マーカー追加") {
                    let newAnnotation = CustomAnnotation(
                        coordinate: CLLocationCoordinate2D(
                            latitude: region.center.latitude + Double.random(in: -0.01...0.01),
                            longitude: region.center.longitude + Double.random(in: -0.01...0.01)
                        ),
                        title: "新しいスポット",
                        subtitle: "追加されたマーカー"
                    )
                    annotations.append(newAnnotation)
                }
            }
            .padding()
        }
    }
}

// MARK: - オーバーレイ例View

/// オーバーレイを表示する例
struct AppKitMapOverlayExampleView: View {
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    )

    var body: some View {
        AppKitMapViewWithOverlays(
            region: $region,
            annotations: [
                CustomAnnotation(
                    coordinate: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
                    title: "中心点"
                )
            ],
            overlays: [
                // 円形オーバーレイ
                MKCircle(
                    center: CLLocationCoordinate2D(latitude: 35.6812, longitude: 139.7671),
                    radius: 500
                )
            ]
        )
    }
}

// MARK: - Preview

#Preview("AppKit Map View") {
    AppKitMapExampleView()
        .frame(width: 800, height: 600)
}

#Preview("AppKit Map with Overlays") {
    AppKitMapOverlayExampleView()
        .frame(width: 800, height: 600)
}
