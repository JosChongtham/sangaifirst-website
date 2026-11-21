// Usage: swift colorfulness.swift img1 img2 ...
// Prints "<mean saturation 0–1>\t<path>" per image. Newspaper scans score low (< ~0.12), photos high.
import Foundation
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("0\t\(path)"); continue }
    let w = 64, h = 64
    var px = [UInt8](repeating: 0, count: w * h * 4)
    let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4,
                        space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
    var total = 0.0
    for i in stride(from: 0, to: px.count, by: 4) {
        let r = Double(px[i]) / 255, g = Double(px[i + 1]) / 255, b = Double(px[i + 2]) / 255
        let mx = max(r, g, b), mn = min(r, g, b)
        total += mx > 0 ? (mx - mn) / mx : 0
    }
    print(String(format: "%.3f\t%@", total / Double(w * h), path))
}
