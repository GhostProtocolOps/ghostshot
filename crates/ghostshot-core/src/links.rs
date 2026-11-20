//! Link coordinate harvester and PDF annotation mapping

#[derive(Debug, Clone, PartialEq)]
pub struct HyperlinkAnnotation {
    pub href: String,
    pub x: f64,
    pub y: f64,
    pub width: f64,
    pub height: f64,
}

#[derive(Debug, Clone)]
pub struct RawLink {
    pub href: String,
    pub viewport_x: f64,
    pub viewport_y: f64,
    pub width: f64,
    pub height: f64,
}

pub struct LinkMapper;

impl LinkMapper {
    /// Maps a link collected during a scroll slice to absolute document coordinates
    pub fn to_document_coords(raw: &RawLink, scroll_x: f64, scroll_y: f64) -> HyperlinkAnnotation {
        HyperlinkAnnotation {
            href: raw.href.clone(),
            x: raw.viewport_x + scroll_x,
            y: raw.viewport_y + scroll_y,
            width: raw.width,
            height: raw.height,
        }
    }

    /// Deduplicates links that span multiple slice steps or overlapping viewports
    pub fn deduplicate(links: Vec<HyperlinkAnnotation>) -> Vec<HyperlinkAnnotation> {
        let mut unique: Vec<HyperlinkAnnotation> = Vec::new();
        for link in links {
            let exists = unique.iter().any(|u| {
                u.href == link.href
                    && (u.x - link.x).abs() < 2.0
                    && (u.y - link.y).abs() < 2.0
            });
            if !exists {
                unique.push(link);
            }
        }
        unique
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_link_mapping() {
        let raw = RawLink {
            href: "https://github.com".to_string(),
            viewport_x: 50.0,
            viewport_y: 120.0,
            width: 150.0,
            height: 24.0,
        };
        let doc_link = LinkMapper::to_document_coords(&raw, 0.0, 1000.0);
        assert_eq!(doc_link.y, 1120.0);
        assert_eq!(doc_link.x, 50.0);
    }

    #[test]
    fn test_link_deduplication() {
        let l1 = HyperlinkAnnotation {
            href: "https://example.com".to_string(),
            x: 10.0,
            y: 200.0,
            width: 100.0,
            height: 20.0,
        };
        let l2 = HyperlinkAnnotation {
            href: "https://example.com".to_string(),
            x: 10.5,
            y: 200.2,
            width: 100.0,
            height: 20.0,
        };
        let l3 = HyperlinkAnnotation {
            href: "https://different.com".to_string(),
            x: 10.0,
            y: 400.0,
            width: 100.0,
            height: 20.0,
        };
        let deduped = LinkMapper::deduplicate(vec![l1, l2, l3]);
        assert_eq!(deduped.len(), 2);
    }
}
