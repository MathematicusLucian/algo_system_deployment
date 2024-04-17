import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { MatSidenav, MatSidenavContainer, MatSidenavContent } from '@angular/material/sidenav';
import { BehaviorSubject } from 'rxjs';
import { SideNavService } from '../../services/sidenav.service';
import { RouterOutlet } from '@angular/router';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'prefab-sidenav',
  templateUrl: 'layout.component.html',
  styleUrl: 'layout.component.scss',
  standalone: true,
  imports: [CommonModule, RouterOutlet, NgFor, MatSidenav, MatSidenavContainer, MatSidenavContent, MatIcon],
})
export class Layout implements OnInit, OnChanges {
  @ViewChild('sidenav', {static: false}) public sidenav!: MatSidenav;
  @Input() pairs$: any = new BehaviorSubject<any[]>([]);
  pairs: any;
  @Input() selectedPair: string = "";
  @Input() open!: boolean | string;
  @Output() pairSelected = new EventEmitter<any>();

  constructor(private sideNavService: SideNavService) { }

  ngOnInit(){ 
    this.sideNavService.sideNavToggleSubject.subscribe(()=> this.sidenav.toggle());
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.pairs = changes["pairs$"]["currentValue"];
  }

  selectPair(pair: string): void {
    this.selectedPair = pair;
    this.pairSelected.emit(this.selectedPair)
  }
}