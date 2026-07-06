use sola_raylib::{color::Color, drawing::RaylibDraw, game_loop};

fn main() {
    let (rl, thread) = sola_raylib::init()
        .size(720, 720)
        .title("Raylib Web")
        .build();

    game_loop::run(rl, thread, 60, |rl, thread| {
        rl.draw(thread, |mut d| {
            d.clear_background(Color::BLACK);
            d.draw_text("Hello, World!", 20, 20, 20, Color::WHITE);
        });
    })
}
