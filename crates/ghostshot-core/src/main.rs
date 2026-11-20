//! GhostShot CLI Companion
//! Demonstrates and benchmarks the high-performance Rust calculations

use ghostshot_core::tiling::TilingEngine;
use ghostshot_core::DocumentDimensions;
use std::time::Instant;

fn main() {
    println!("====================================================");
    println!("  GhostShot Core Engine (Rust v0.1.0)");
    println!("  High-Throughput Scroll & Tile Mathematics");
    println!("====================================================");

    // Benchmark a 50,000px height page with 2x Retina DPI
    let start = Instant::now();
    let dims = DocumentDimensions::new(1920.0, 50000.0, 1920.0, 1080.0, 2.0);
    let slices = dims.plan_scroll_slices();
    let (phys_w, phys_h) = dims.physical_pixels();

    let tiling = TilingEngine::new(16384);
    let tiles = tiling.calculate_tiles(phys_w as u32, phys_h as u32, dims.dpr);
    let elapsed = start.elapsed();

    println!("Document: 1920x50000 @ 2x DPR");
    println!("Physical canvas required: {} x {} px ({} Megapixels)", phys_w, phys_h, (phys_w * phys_h) / 1_000_000);
    println!("Calculated {} scroll slices in {:?}", slices.len(), elapsed);
    println!("Canvas split into {} safe tiles (Max limit 16384px):", tiles.len());
    for (i, t) in tiles.iter().enumerate() {
        println!("  Tile #{}: y = {}, height = {} px", i, t.source_y, t.height);
    }
    println!("\nRust calculations executed in {:?}", elapsed);
    println!("Engine status: OK.");
}
