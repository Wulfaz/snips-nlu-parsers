# rmp-serde 0.13.7 (vendored)

Unmodified `src/` and `Cargo.toml` of rmp-serde 0.13.7 (MIT license,
https://github.com/3Hren/msgpack-rust), from
https://static.crates.io/crates/rmp-serde/rmp-serde-0.13.7.crate
(sha256 011e1d58446e9fa3af7cdc1fb91295b10621d3ac4cb3a85cc86385ee9ca50cd3,
as recorded by crates.io). Tests and benches are left out.

Why: gazetteer-entity-parser 0.8.0 requires `rmp-serde = "^0.13"`, and every
0.13.x release is yanked from crates.io, so Cargo cannot resolve it anymore.
gazetteer-entity-parser 0.9.0 uses rmp-serde 1.x but changed its
serialization format, so it cannot load existing gazetteer entity resources.
The root Cargo.toml substitutes this copy through `[patch.crates-io]`.
It still calls `rmp::decode::read_data_*`, removed in rmp 0.8.15: rmp is
pinned to 0.8.14 in Cargo.lock.
