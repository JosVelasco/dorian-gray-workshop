#!/usr/bin/env python3
"""
Build blueprint.json for the Dorian Gray Code Workshop.
Run after any change to mu-plugin.php to keep the inline copy current.
"""
import json

with open('mu-plugin.php', 'r') as f:
    mu_plugin_content = f.read()

# ── Checklist + pages PHP ─────────────────────────────────────────────────────
setup_php = r"""<?php
require_once '/wordpress/wp-load.php';

$upload_dir = wp_upload_dir();
$hero_file  = $upload_dir['basedir'] . '/hero-landscape.jpg';
$filetype   = wp_check_filetype( basename( $hero_file ), null );

$attachment = array(
    'guid'           => $upload_dir['baseurl'] . '/hero-landscape.jpg',
    'post_mime_type' => $filetype['type'],
    'post_title'     => 'Hero Landscape',
    'post_content'   => '',
    'post_status'    => 'inherit',
);
$hero_id = wp_insert_attachment( $attachment, $hero_file );

require_once ABSPATH . 'wp-admin/includes/image.php';
$attach_data = wp_generate_attachment_metadata( $hero_id, $hero_file );
wp_update_attachment_metadata( $hero_id, $attach_data );
$hero_url = wp_get_attachment_url( $hero_id );

// --- Elementor page ---
$el_data = json_encode( array(
    array(
        'id'       => 'a1b2c3d4',
        'elType'   => 'section',
        'isInner'  => false,
        'settings' => array(
            'background_background' => 'classic',
            'background_image'      => array(
                'url'    => $hero_url,
                'id'     => $hero_id,
                'alt'    => '',
                'source' => 'library',
            ),
            'background_size'     => 'cover',
            'background_position' => 'center center',
            'height'              => 'min-height',
            'custom_height'       => array( 'unit' => 'vh', 'size' => 70, 'sizes' => array() ),
            'content_position'    => 'middle',
        ),
        'elements' => array(
            array(
                'id'       => 'e1f2g3h4',
                'elType'   => 'column',
                'isInner'  => false,
                'settings' => array( '_column_size' => 100, 'content_position' => 'middle' ),
                'elements' => array(
                    array(
                        'id'         => 'i1j2k3l4',
                        'elType'     => 'widget',
                        'isInner'    => false,
                        'widgetType' => 'heading',
                        'settings'   => array(
                            'title'                 => 'Beautiful. Responsive. Or Is It?',
                            'title_color'           => '#ffffff',
                            'typography_typography' => 'custom',
                            'typography_font_size'  => array( 'unit' => 'px', 'size' => 48, 'sizes' => array() ),
                            'align'                 => 'center',
                        ),
                    ),
                    array(
                        'id'         => 'm1n2o3p4',
                        'elType'     => 'widget',
                        'isInner'    => false,
                        'widgetType' => 'text-editor',
                        'settings'   => array(
                            'editor' => '<p style="color: #ffffff; font-size: 20px; text-align: center;">This hero image looks perfect. Open DevTools Network tab to see what the browser actually downloaded.</p>',
                        ),
                    ),
                ),
            ),
        ),
    ),
), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );

$elementor_page_id = wp_insert_post( array(
    'post_title'     => 'Elementor Page',
    'post_name'      => 'elementor-page',
    'post_status'    => 'publish',
    'post_type'      => 'page',
    'comment_status' => 'closed',
) );
update_post_meta( $elementor_page_id, '_elementor_edit_mode',     'builder' );
update_post_meta( $elementor_page_id, '_elementor_template_type', 'wp-page' );
update_post_meta( $elementor_page_id, '_elementor_version',       '3.35.5' );
update_post_meta( $elementor_page_id, '_elementor_data', wp_slash( $el_data ) );

// --- Native editor page ---
$cover  = '<!-- wp:cover {"url":"' . $hero_url . '","id":' . $hero_id . ',"dimRatio":40,"minHeight":70,"minHeightUnit":"vh","isDark":false,"align":"full"} -->';
$cover .= '<div class="wp-block-cover alignfull" style="min-height:70vh">';
$cover .= '<span aria-hidden="true" class="wp-block-cover__background has-background-dim-40 has-background-dim"></span>';
$cover .= '<img class="wp-block-cover__image-background wp-image-' . $hero_id . '" alt="" src="' . $hero_url . '" data-object-fit="cover"/>';
$cover .= '<div class="wp-block-cover__inner-container">';
$cover .= '<!-- wp:heading {"textAlign":"center","style":{"color":{"text":"#ffffff"}}} -->';
$cover .= '<h2 class="wp-element-heading has-text-align-center has-text-color" style="color:#ffffff">Beautiful. Responsive. And Actually Responsive.</h2>';
$cover .= '<!-- /wp:heading -->';
$cover .= '<!-- wp:paragraph {"align":"center","style":{"color":{"text":"#ffffff"}}} -->';
$cover .= '<p class="has-text-align-center has-text-color" style="color:#ffffff">This hero image looks identical. View page source and search for srcset. Then compare with the Elementor page.</p>';
$cover .= '<!-- /wp:paragraph -->';
$cover .= '</div></div>';
$cover .= '<!-- /wp:cover -->';

$native_page_id = wp_insert_post( array(
    'post_title'     => 'Native Editor',
    'post_name'      => 'native-editor',
    'post_status'    => 'publish',
    'post_type'      => 'page',
    'post_content'   => $cover,
    'comment_status' => 'closed',
) );

// --- Checklist page ---
$checklist_pid = wp_insert_post( array(
    'post_title'     => 'Workshop Checklist',
    'post_name'      => 'workshop-checklist',
    'post_status'    => 'publish',
    'post_type'      => 'page',
    'post_content'   => '',
    'comment_status' => 'closed',
) );

$ep_url      = home_url( '/elementor-page/' );
$ne_url      = home_url( '/native-editor/' );
$plugins_url = admin_url( 'plugins.php' );

$c  = '<!-- wp:paragraph --><p>You are about to audit two pages that look identical to any visitor. One was built with Elementor, one with the native editor. Open DevTools and follow the tasks below to discover what is really happening.</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 1: Audit the Elementor Page</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Open <a href="' . $ep_url . '">/elementor-page/</a>. Open DevTools (Windows: Ctrl+Shift+I, Mac: Cmd+Option+I) and go to the Network tab. Reload the page. Note the total number of requests, number of CSS files, and total image weight.</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> How many requests does Elementor make? How many are CSS files?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 2: Audit the Native Editor Page</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Open <a href="' . $ne_url . '">/native-editor/</a>. Same process: Network tab, reload. Compare the total page weight and request count with Task 1.</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> What changed? What stayed the same?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 3: Find the srcset on the Native Editor Page</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>On <a href="' . $ne_url . '">/native-editor/</a>, right-click and choose View Page Source. Search for srcset. What do you find? How many image size variants are listed?</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> Why does the browser need multiple image sizes?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 4: Look for srcset on the Elementor Page</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Do the same on <a href="' . $ep_url . '">/elementor-page/</a>. View Page Source and search for srcset near the background image. What do you find?</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> What does this mean for a visitor on a mobile device on a slow connection?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Task 5: The Deactivation Test</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Go to <a href="' . $plugins_url . '">Plugins</a> and deactivate Elementor. Then reload <a href="' . $ne_url . '">/native-editor/</a> and open the Network tab. How many requests now? What disappeared?</p><!-- /wp:paragraph -->';
$c .= '<!-- wp:paragraph --><p><strong>Discussion:</strong> This page was not built with Elementor. Why was it loading Elementor assets?</p><!-- /wp:paragraph -->';

$c .= '<!-- wp:heading --><h2 class="wp-block-heading">Your Conclusions</h2><!-- /wp:heading -->';
$c .= '<!-- wp:paragraph --><p>Write your three main conclusions about the differences between Elementor and the native editor.</p><!-- /wp:paragraph -->';

wp_update_post( array( 'ID' => $checklist_pid, 'post_content' => $c ) );
"""

# ── Quiz PHP ──────────────────────────────────────────────────────────────────
quiz_php = r"""<?php
require_once '/wordpress/wp-load.php';

global $wpdb;

$wpdb->insert( $wpdb->prefix . 'mlw_quizzes', array(
    'quiz_name'          => 'Dorian Gray Code Workshop: Knowledge Check',
    'randomness_order'   => 2,
    'show_score'         => 1,
    'total_user_tries'   => 0,
    'ajax_show_correct'  => 1,
    'require_log_in'     => 0,
    'user_name'          => 2,
    'user_comp'          => 2,
    'user_email'         => 2,
    'user_phone'         => 2,
    'comment_section'    => 1,
    'deleted'            => 0,
    'quiz_views'         => 0,
    'quiz_taken'         => 0,
    'last_activity'      => current_time( 'mysql' ),
    'submit_button_text' => 'Submit Answers',
    'message_before'     => '',
    'message_after'      => '',
) );
$quiz_id = $wpdb->insert_id;

function dg_q( $quiz_id, $text, $answers, $correct_idx ) {
    global $wpdb;
    $arr = array();
    foreach ( $answers as $i => $a ) {
        $arr[] = array( $a, ( $i === $correct_idx ) ? 1 : 0, ( $i === $correct_idx ) ? 1 : 0, '' );
    }
    $wpdb->insert( $wpdb->prefix . 'mlw_questions', array(
        'quiz_id'               => $quiz_id,
        'question_name'         => $text,
        'answer_array'          => maybe_serialize( $arr ),
        'correct_answer'        => $correct_idx + 1,
        'question_type'         => 0,
        'question_type_new'     => '0',
        'question_order'        => 0,
        'comments'              => 1,
        'question_settings'     => maybe_serialize( array( 'Required' => '0' ) ),
        'deleted'               => 0,
        'deleted_question_bank' => 0,
    ) );
    return $wpdb->insert_id;
}

$qids = array();

$qids[] = dg_q( $quiz_id,
    'What does the srcset attribute on an img tag do?',
    array(
        'Adds a caption below the image',
        'Provides multiple image sizes so the browser can download the most appropriate one for the screen',
        'Makes the image load faster by compressing it on the server',
        'Prevents the image from being saved by right-clicking',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'The native editor page has srcset but the Elementor page does not. What does this mean for a visitor on a slow mobile connection?',
    array(
        'The Elementor page loads faster because it has fewer attributes to process',
        'The native editor page is harder to maintain',
        'The Elementor page forces every visitor to download the full-resolution image regardless of their screen size',
        'Both pages behave identically on mobile devices',
    ),
    2
);

$qids[] = dg_q( $quiz_id,
    'Why does Elementor use a CSS background-image for the hero instead of an img tag?',
    array(
        'CSS background images load faster than img tags',
        'It gives designers more styling control, but the browser cannot generate a srcset for CSS backgrounds',
        'WordPress blocks img tags inside page builder sections',
        'CSS backgrounds are automatically optimised by the browser',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'After deactivating Elementor, what happened to the request count on the native editor page?',
    array(
        'It increased because WordPress had to compensate for the missing plugin',
        'It stayed the same because Elementor assets are cached by the browser',
        'It decreased -- Elementor CSS and JS files that were loading unnecessarily disappeared',
        'The page stopped working entirely',
    ),
    2
);

$qids[] = dg_q( $quiz_id,
    'Why was the native editor page loading Elementor assets even though it was not built with Elementor?',
    array(
        'WordPress automatically loads all active plugin assets on every front-end page',
        'The native editor uses Elementor as a rendering fallback',
        'The page template was originally created in Elementor',
        'Elementor only loads its assets on pages where it detects a form',
    ),
    0
);

$qids[] = dg_q( $quiz_id,
    'What does the total transfer size shown in the DevTools Network tab represent?',
    array(
        'The number of database queries the page makes',
        'The combined size of all files the browser downloads to render the page',
        'The time it takes for the first byte to arrive from the server',
        'The number of HTTP redirects before the page loads',
    ),
    1
);

$qids[] = dg_q( $quiz_id,
    'Which of these is a direct performance advantage of using the native WordPress editor over Elementor?',
    array(
        'The native editor produces pages with fewer HTTP requests and no unnecessary plugin assets',
        'The native editor automatically minifies JavaScript',
        'Pages built with the native editor cannot be edited after publishing',
        'The native editor disables caching plugins automatically',
    ),
    0
);

$qids[] = dg_q( $quiz_id,
    'What is the main lesson of the Deactivation Test in this workshop?',
    array(
        'Plugins should always be deleted, not just deactivated',
        'Elementor is incompatible with WordPress 6.9',
        'Every active plugin can add overhead to pages it has no role on -- audit what loads on every page',
        'The native editor requires more plugins to match Elementor features',
    ),
    2
);

$wpdb->update(
    $wpdb->prefix . 'mlw_quizzes',
    array( 'quiz_settings' => maybe_serialize( array(
        'pages'                  => array( $qids ),
        'enable_quick_result_mc' => 1,
    ) ) ),
    array( 'quiz_id' => $quiz_id )
);

$quiz_post_id = wp_insert_post( array(
    'post_title'   => 'Dorian Gray Code Workshop: Knowledge Check',
    'post_content' => '[mlw_quizmaster quiz=' . $quiz_id . ']',
    'post_status'  => 'publish',
    'post_author'  => get_current_user_id(),
    'post_type'    => 'qsm_quiz',
) );
add_post_meta( $quiz_post_id, 'quiz_id', intval( $quiz_id ) );

$kid = wp_insert_post( array(
    'post_title'   => 'Knowledge Check',
    'post_name'    => 'knowledge-check',
    'post_status'  => 'publish',
    'post_type'    => 'page',
    'post_content' => '',
) );
$shortcode = '[mlw_quizmaster quiz=' . $quiz_id . ']';
$k  = '<!-- wp:paragraph --><p>Eight questions based on what you just explored. Click an answer to see immediately whether you were right.</p><!-- /wp:paragraph -->';
$k .= '<!-- wp:shortcode -->' . $shortcode . '<!-- /wp:shortcode -->';
wp_update_post( array( 'ID' => $kid, 'post_content' => $k ) );

$checklist = get_page_by_path( 'workshop-checklist' );
if ( $checklist ) {
    $quiz_url = get_permalink( $kid );
    $q  = '<!-- wp:separator --><hr class="wp-block-separator has-alpha-channel-opacity"/><!-- /wp:separator -->';
    $q .= '<!-- wp:heading {"level":2} --><h2 class="wp-block-heading">Knowledge Check</h2><!-- /wp:heading -->';
    $q .= '<!-- wp:paragraph --><p>Finished all five tasks? Head to the <a href="' . $quiz_url . '">Knowledge Check</a> to confirm what you have learned.</p><!-- /wp:paragraph -->';
    wp_update_post( array( 'ID' => $checklist->ID, 'post_content' => $checklist->post_content . $q ) );
}

echo 'quiz done';
"""

# ── Blueprint ─────────────────────────────────────────────────────────────────
blueprint = {
    "$schema": "https://playground.wordpress.net/blueprint-schema.json",
    "landingPage": "/wp-admin",
    "login": True,
    "preferredVersions": {
        "php": "8.2",
        "wp": "6.9"
    },
    "steps": [
        # Suppress Elementor onboarding before install
        {
            "step": "wp-cli",
            "command": "wp option update elementor_onboarded 1 --allow-root"
        },
        {
            "step": "wp-cli",
            "command": "wp option update elementor_install_time 1 --allow-root"
        },
        {
            "step": "wp-cli",
            "command": "wp option update elementor_onboarding_opt_in yes --allow-root"
        },
        # Theme
        {
            "step": "installTheme",
            "themeData": {
                "resource": "wordpress.org/themes",
                "slug": "hello-elementor"
            },
            "options": {"activate": True}
        },
        # Plugins
        {
            "step": "wp-cli",
            "command": "wp user meta update 1 elementor_introduction '{\"e-editor-one-notice-pointer\":true}' --format=json --allow-root"
        },
        {
            "step": "installPlugin",
            "pluginData": {
                "resource": "wordpress.org/plugins",
                "slug": "elementor"
            }
        },
        {
            "step": "installPlugin",
            "pluginData": {
                "resource": "wordpress.org/plugins",
                "slug": "quiz-master-next"
            }
        },
        # Disable QSM new render mode
        {
            "step": "wp-cli",
            "command": "wp option update qmn-settings '{\"enable_new_render\":0}' --format=json --allow-root"
        },
        # Images
        {
            "step": "mkdir",
            "path": "/wordpress/wp-content/uploads"
        },
        {
            "step": "writeFile",
            "path": "/wordpress/wp-content/uploads/hero-landscape.jpg",
            "data": {
                "resource": "url",
                "url": "https://cdn.jsdelivr.net/gh/JosVelasco/dorian-gray-workshop@main/hero-landscape.jpg"
            }
        },
        {
            "step": "writeFile",
            "path": "/wordpress/wp-content/uploads/dorian-wp-workshop.jpg",
            "data": {
                "resource": "url",
                "url": "https://cdn.jsdelivr.net/gh/JosVelasco/dorian-gray-workshop@main/dorian-wp-workshop.jpg"
            }
        },
        # Create pages
        {
            "step": "runPHP",
            "code": setup_php
        },
        # mu-plugin (inlined)
        {
            "step": "mkdir",
            "path": "/wordpress/wp-content/mu-plugins"
        },
        {
            "step": "writeFile",
            "path": "/wordpress/wp-content/mu-plugins/dorian-workshop.php",
            "data": mu_plugin_content
        },
        # Quiz
        {
            "step": "runPHP",
            "code": quiz_php
        },
    ]
}

with open('blueprint.json', 'w') as f:
    json.dump(blueprint, f, indent=2, ensure_ascii=False)

print("blueprint.json written.")
print(f"mu-plugin.php inlined: {len(mu_plugin_content)} chars")
