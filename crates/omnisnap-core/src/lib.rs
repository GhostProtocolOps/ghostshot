//! OmniSnap Core Engine (Rust)
//! High-performance slice coordinate math, canvas tiling splits, and hyperlink coordinate transformation.

pub mod tiling;
pub mod links;

/// Represents a single captured viewport slice
#[derive(Debug, Clone, PartialEq)]
pub struct CaptureSlice {
    pub index: usize,
    pub x: f64,
    pub y: f64,
    pub width: f64,
    pub height: f64,
    pub dpr: f64,
}

/// Represents the overall document dimension
#[derive(Debug, Clone, PartialEq)]
pub struct DocumentDimensions {
    pub full_width: f64,
    pub full_height: f64,
    pub window_width: f64,
    pub window_height: f64,
    pub dpr: f64,
}

impl DocumentDimensions {
    pub fn new(full_width: f64, full_height: f64, window_width: f64, window_height: f64, dpr: f64) -> Self {
        Self {
            full_width,
            full_height,
            window_width,
            window_height,
            dpr: if dpr <= 0.0 { 1.0 } else { dpr },
        }
    }

    /// Calculate the total physical pixels taking DPR into account
    pub fn physical_pixels(&self) -> (u64, u64) {
        let w = (self.full_width * self.dpr).ceil() as u64;
        let h = (self.full_height * self.dpr).ceil() as u64;
        (w, h)
    }

    /// Generate an optimal sequence of scroll step coordinates
    pub fn plan_scroll_slices(&self) -> Vec<CaptureSlice> {
        let mut slices = Vec::new();
        let mut curr_y = 0.0;
        let mut idx = 0;

        let step_y = self.window_height;
        while curr_y < self.full_height {
            let slice_h = if curr_y + step_y > self.full_height {
                self.full_height - curr_y
            } else {
                step_y
            };

            slices.push(CaptureSlice {
                index: idx,
                x: 0.0,
                y: curr_y,
                width: self.window_width,
                height: slice_h,
                dpr: self.dpr,
            });

            curr_y += step_y;
            idx += 1;
        }

        if slices.is_empty() {
            slices.push(CaptureSlice {
                index: 0,
                x: 0.0,
                y: 0.0,
                width: self.window_width,
                height: self.window_height,
                dpr: self.dpr,
            });
        }

        slices
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scroll_slices_planning() {
        let dims = DocumentDimensions::new(1280.0, 3600.0, 1280.0, 1000.0, 2.0);
        let slices = dims.plan_scroll_slices();
        
        assert_eq!(slices.len(), 4);
        assert_eq!(slices[0].y, 0.0);
        assert_eq!(slices[0].height, 1000.0);
        assert_eq!(slices[1].y, 1000.0);
        assert_eq!(slices[2].y, 2000.0);
        assert_eq!(slices[3].y, 3000.0);
        assert_eq!(slices[3].height, 600.0);
    }

    #[test]
    fn test_physical_pixels() {
        let dims = DocumentDimensions::new(1000.0, 2500.0, 1000.0, 1000.0, 2.0);
        let (pw, ph) = dims.physical_pixels();
        assert_eq!(pw, 2000);
        assert_eq!(ph, 5000);
    }
}
