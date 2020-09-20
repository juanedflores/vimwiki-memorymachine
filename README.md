# Vimwiki Memory Machine

## What it does
This simple plugin is meant to work with vimwiki to inform a user what wikis are most visited, and most developed.

## Requirements
* python3 support
* vimwiki

## Installation
Example with vim-plug:
```
Plug 'juaneduardoflores/vimwiki-memorymachine', { 'do': ':UpdateRemotePlugins' }
```

## How to Use
Variables to define:
```
let g:MemMachineEnable = 0
let g:MemMachineIndex = "/Path/To/Your/MemMachineWiki.md"
```
Commands:
```
:MemMachineToggle - Toggle Plugin
```

### Inspiration

This plugin is inspired by the well known 1945 essay "As We May Think" published in The Atlantic written by Vannevar Bush: https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/

Because I use vimwiki to save my notes, whether its to learn programming, german, or history, I have found that storing what I perceive as things I "learned" in my computer memory is often not a good representation of my human brain memory. This plugin is a dream project to make vimwiki add stats to somewhat visually represent my human memory and the likeliness in strength that I truly "know" or remember the contents in a wiki by being able to see what needs more attention or reinforcement.





