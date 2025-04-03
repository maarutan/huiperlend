-- ██╗███╗   ██╗██╗████████╗
-- ██║████╗  ██║██║╚══██╔══╝
-- ██║██╔██╗ ██║██║   ██║
-- ██║██║╚██╗██║██║   ██║
-- ██║██║ ╚████║██║   ██║
-- ╚═╝╚═╝  ╚═══╝╚═╝   ╚═╝
--

require("relative-motions"):setup({ show_numbers = "relative_absolute", show_motion = true })
require("eza-preview"):setup({
	level = 3,
	follow_symlinks = false,
	dereference = false,
})
require("keycalm").setup({
	limit = 10, -- Number of presses before blocking
	delay = 3, -- Block duration in seconds (also notification duration)
	notify_title = "Hold it, {user}!", -- Notification title
	notify_message = "🤠 Take it easy, cowboy!", -- Blocking message
	notify_unblock = "{key} 🥳", -- Unblock message
})

require("full-border"):setup({
	THEME.manager.border_style.fg,
	border_style = ui.Style():fg(THEME.manager.border_style.fg or "black"),

	type = ui.Border.PLAIN,
})

require("smart-enter"):setup({

	open_multi = true,
})
-- if os.getenv("NVIM") then
-- 	require("hide-preview"):entry()
-- end
THEME.git = THEME.git
	or {
		-- Colours
		modified = ui.Style():fg("#0096DB"),
		added = ui.Style():fg("#239549"),
		untracked = ui.Style():fg("#B0B0B0"),
		ignored = ui.Style():fg("#B0B0B0"),
		deleted = ui.Style():fg("#D32752"),

		-- Unmerged
		updated = ui.Style():fg("#CD32C0"),

		-- Icons
		modified_sign = "  ",
		added_sign = "  ",
		untracked_sign = "  ",
		ignored_sign = "  ",
		deleted_sign = "  ",

		-- Unmerged
		updated_sign = "  ",
	}

-- Set up the git plugin
require("git"):setup()

local themes = require("yatline-catppuccin"):setup("macchiato") -- "latte" | "frappe" | "macchiato"
-- local themes = require("yatline-gruvbox"):setup("light") -- or "light"
require("yatline"):setup({
	theme = themes,
	section_separator = { open = "", close = "" },
	part_separator = { open = "", close = "" },
	inverse_separator = { open = "", close = "" },

	style_a = {
		fg = "black",
		bg_mode = {
			normal = "blue",
			select = "brightyellow",
			un_set = "brightred",
		},
	},
	style_b = { bg = "brightblack", fg = "brightwhite" },
	style_c = { bg = "black", fg = "brightwhite" },

	permissions_t_fg = "green",
	permissions_r_fg = "yellow",
	permissions_w_fg = "red",
	permissions_x_fg = "cyan",
	permissions_s_fg = "white",

	tab_width = 20,
	tab_use_inverse = false,

	selected = { icon = "󰻭", fg = "yellow" },
	copied = { icon = "", fg = "green" },
	cut = { icon = "", fg = "red" },

	total = { icon = "󰮍", fg = "yellow" },
	succ = { icon = "", fg = "green" },
	fail = { icon = "", fg = "red" },
	found = { icon = "󰮕", fg = "blue" },
	processed = { icon = "󰐍", fg = "green" },

	show_background = false,

	display_header_line = true,
	display_status_line = true,

	component_positions = { "header", "tab", "status" },

	header_line = {
		left = {
			section_a = {
				{ type = "coloreds", custom = true, name = { { " ~~> ", "black" } } },
				{ type = "string", custom = false, name = "hovered_path" },
			},
			section_b = {},
			section_c = {},
		},
		right = {
			section_a = {},
			section_b = {
				{ type = "line", custom = false, name = "tabs", params = { "left" } },
			},
			section_c = {
				{ type = "coloreds", custom = true, name = { { "  󰇥  ", "while" } } },
			},
		},
	},

	status_line = {
		left = {
			section_a = {
				{ type = "string", custom = false, name = "tab_mode" },
			},
			section_b = {
				{ type = "string", custom = false, name = "hovered_size" },
			},
			section_c = {
				-- { type = "string", custom = false, name = "hovered_path" },
				{ type = "coloreds", custom = false, name = "count" },
			},
		},
		right = {
			section_a = {
				{ type = "string", custom = false, name = "cursor_position" },
			},
			section_b = {
				{ type = "string", custom = false, name = "cursor_percentage" },
			},
			section_c = {
				{ type = "string", custom = false, name = "hovered_file_extension", params = { true } },
				{ type = "coloreds", custom = false, name = "permissions" },
			},
		},
	},
}) -- local gruvbox_theme = require("yatline-gruvbox"):setup("light") -- or "light"

-- Using the default configuration
require("augment-command"):setup({
	prompt = false,
	default_item_group_for_prompt = "hovered",
	smart_enter = true,
	smart_paste = false,
	smart_tab_create = false,
	smart_tab_switch = false,
	confirm_on_quit = true,
	open_file_after_creation = false,
	enter_directory_after_creation = false,
	use_default_create_behaviour = false,
	enter_archives = true,
	extract_retries = 3,
	recursively_extract_archives = true,
	preserve_file_permissions = false,
	must_have_hovered_item = true,
	skip_single_subdirectory_on_enter = true,
	skip_single_subdirectory_on_leave = true,

	-- scroll
	scroll_delay = 0.02,
	smooth_scrolling = true,
	wraparound_file_navigation = true,
})
require("simple-tag"):setup({
	-- UI display mode (icon, text, hidden)
	ui_mode = "icon", -- (Optional)

	-- Disable tag key hints (popup in bottom right corner)
	hints_disabled = false, -- (Optional)

	-- linemode order: adjusts icon/text position. Fo example, if you want icon to be on the mose left of linemode then set linemode_order larger than 1000.
	-- More info: https://github.com/sxyazi/yazi/blob/077faacc9a84bb5a06c5a8185a71405b0cb3dc8a/yazi-plugin/preset/components/linemode.lua#L4-L5
	linemode_order = 500, -- (Optional)

	-- You can backup/restore this folder. But don't use backed up folder in the different OS.
	-- save_path =  -- full path to save tags folder (Optional)
	--       - Linux/MacOS: os.getenv("HOME") .. "/.config/yazi/tags"
	--       - Windows: os.getenv("APPDATA") .. "\\yazi\\config\\tags"

	-- Set tag colors
	colors = { -- (Optional)
		-- Set this same value with `theme.toml` > [manager] > hovered > reversed
		-- Default theme use "reversed = true".
		-- More info: https://github.com/sxyazi/yazi/blob/077faacc9a84bb5a06c5a8185a71405b0cb3dc8a/yazi-config/preset/theme-dark.toml#L25
		reversed = true, -- (Optional)

		-- More colors: https://yazi-rs.github.io/docs/configuration/theme#types.color
		-- format: [tag key] = "color"
		["*"] = "#bf68d9", -- (Optional)
		["$"] = "green",
		["!"] = "#cc9057",
		["1"] = "cyan",
		["p"] = "red",
	},

	-- Set tag icons. Only show when ui_mode = "icon".
	-- Any text or nerdfont icons should work
	-- Default icon from mactag.yazi: ●; , , 󱈤
	-- More icon from nerd fonts: https://www.nerdfonts.com/cheat-sheet
	icons = { -- (Optional)
		-- default icon
		default = "󰚋",

		-- format: [tag key] = "tag icon"
		["*"] = "*",
		["$"] = "",
		["!"] = "",
		["p"] = "",
	},
})
