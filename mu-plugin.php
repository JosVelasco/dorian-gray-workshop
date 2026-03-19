<?php
/**
 * Plugin Name: Dorian Gray Workshop
 * Description: Must-use plugin for The Dorian Gray Code Workshop
 */

// Load Google Fonts in admin head (for notice chrome)
add_action( 'admin_head', function () {
	echo '<link rel="preconnect" href="https://fonts.googleapis.com">';
	echo '<link href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@1&family=Cinzel:wght@600&display=swap" rel="stylesheet">';
} );

// Load fonts inside the block editor canvas
add_action( 'enqueue_block_editor_assets', function () {
	echo '<link href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@1&family=Cinzel:wght@600&display=swap" rel="stylesheet">';
	wp_add_inline_style( 'wp-block-library', '
		.editor-styles-wrapper p,
		.wp-block-post-content p {
			font-size: 21px !important;
			font-family: "IM Fell English", serif !important;
			font-style: italic !important;
		}
		.editor-styles-wrapper h2 {
			font-family: "Cinzel", serif !important;
			font-weight: 600 !important;
		}
	' );
} );

// Admin notice with banner, bullets, and checklist link
add_action( 'admin_notices', function () {
	$checklist = get_page_by_path( 'workshop-checklist' );
	$url       = $checklist ? get_edit_post_link( $checklist->ID ) : admin_url();
	$img       = content_url( 'uploads/dorian-wp-workshop.jpg' );
	?>
	<div style="background:#1a1a1a;border:4px solid #b8960c;margin:10px 0 20px;overflow:hidden;">
		<img src="<?php echo esc_url( $img ); ?>" alt="The Dorian Gray Code Workshop" style="display:block;width:100%;height:auto;">
		<div style="padding:16px 24px;color:#e8dcc8;">
			<p style="font-family:'IM Fell English',serif;font-style:italic;font-size:22px;font-weight:normal;margin:0 0 14px;line-height:1.8;color:#e8dcc8;">Perfection is only skin deep. Open DevTools, and the portrait reveals all: phantom requests, unused CSS, and images the browser cannot resize.</p>
			<a href="<?php echo esc_url( $url ); ?>" style="font-family:'Cinzel',serif;color:#d4a843;font-size:22px;font-weight:600;text-decoration:underline;">&rarr; Open Workshop Checklist</a>
		</div>
	</div>
	<?php
} );

// Disable Gutenberg everywhere except the checklist page
add_filter( 'use_block_editor_for_post', function ( $use_block_editor, $post ) {
	return $post->post_name === 'workshop-checklist';
}, 10, 2 );

// Quiz styles loaded in footer to override QSM's own stylesheet.
add_action( 'wp_footer', function () {
	echo '<style>
		.qsm-quiz-container.qmn_quiz_container .mlw_qmn_question p { font-weight: bold !important; }
		.qsm-submit-btn { display: none !important; }
		.mlw_custom_start { display: none !important; }
		.mlw_previous { display: none !important; }
		.quiz_section.qsm-question-wrapper { margin-bottom: 30px; }
	</style>';
}, 99 );
