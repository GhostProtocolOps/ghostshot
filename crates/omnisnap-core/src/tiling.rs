//! Canvas Tiling and Memory Boundary Calculator
//! Solves browser canvas pixel limits (e.g. 16,384px or 32,767px height limit).

/// Maximum safe canvas dimension in Chromium and WebKit (Safari)
pub const DEFAULT_MAX_CANVAS_DIMENSION: u32 = 16384;

#[derive(Debug, Clone, PartialEq)]
pub struct CanvasTile {
    pub tile_index: usize,
    pub source_y: u32,
    pub width: u32,
    pub height: u32,
    pub dpr: f64,
}

pub struct TilingEngine {
    max_dimension: u32,
}

impl TilingEngine {
    pub fn new(max_dimension: u32) -> Self {
        Self {
            max_dimension: if max_dimension == 0 { DEFAULT_MAX_CANVAS_DIMENSION } else { max_dimension },
        }
    }

    /// Split a tall pixel height into a series of safe canvas tiles
    pub fn calculate_tiles(&self, total_width_px: u32, total_height_px: u32, dpr: f64) -> Vec<CanvasTile> {
        let mut tiles = Vec::new();
        let mut curr_y = 0;
        let mut index = 0;

        while curr_y < total_height_px {
            let remaining = total_height_px - curr_y;
            let tile_h = if remaining > self.max_dimension {
                self.max_dimension
            } else {
                remaining
            };

            tiles.push(CanvasTile {
                tile_index: index,
                source_y: curr_y,
                width: total_width_px,
                height: tile_h,
                dpr,
            });

            curr_y += tile_h;
            index += 1;
        }

        if tiles.is_empty() {
            tiles.push(CanvasTile {
                tile_index: 0,
                source_y: 0,
                width: total_width_px,
                height: total_height_px,
                dpr,
            });
        }

        tiles
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tiling_below_limit() {
        let engine = TilingEngine::new(16384);
        let tiles = engine.calculate_tiles(2560, 10000, 2.0);
        assert_eq!(tiles.len(), 1);
        assert_eq!(tiles[0].height, 10000);
        assert_eq!(tiles[0].source_y, 0);
    }

    #[test]
    fn test_tiling_exceeding_limit() {
        let engine = TilingEngine::new(16384);
        let tiles = engine.calculate_tiles(2560, 40000, 2.0);
        assert_eq!(tiles.len(), 3);
        assert_eq!(tiles[0].height, 16384);
        assert_eq!(tiles[0].source_y, 0);
        assert_eq!(tiles[1].height, 16384);
        assert_eq!(tiles[1].source_y, 16384);
        assert_eq!(tiles[2].height, 7232);
        assert_eq!(tiles[2].source_y, 32768);
    }
}
